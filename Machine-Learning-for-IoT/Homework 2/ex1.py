import uuid
import time
import sounddevice as sd
import numpy as np
from threading import Thread
import tensorflow as tf
import adafruit_dht
from board import D4
from scipy import signal
import redis
import argparse

# Parse command-line arguments for Redis connection
parser = argparse.ArgumentParser(description="Temperature and Humidity Monitoring with Redis TimeSeries")
parser.add_argument("--host", required=True, help="Redis Cloud host")
parser.add_argument("--port", type=int, required=True, help="Redis Cloud port")
parser.add_argument("--user", required=True, help="Redis Cloud username")
parser.add_argument("--password", required=True, help="Redis Cloud password")
args = parser.parse_args()

# Connect to Redis
redis_client = redis.Redis(
    host=args.host,
    port=args.port,
    username=args.user,
    password=args.password
)

dht_device = adafruit_dht.DHT11(D4)

mac_address = hex(uuid.getnode())
one_day_in_ms = 24 * 60 * 60 * 1000
temperature_key = f'{mac_address}:temperature'
humidity_key = f'{mac_address}:humidity'

try:
    redis_client.ts().create(temperature_key, retention_msecs=30 * one_day_in_ms)
    redis_client.ts().create(humidity_key, retention_msecs=30 * one_day_in_ms)
except redis.ResponseError as e:
    print("Error creating TimeSeries or rules:", e)

recording_samplerate = 48000
vad_sample_rate = 16000

PREPROCESSING_ARGS = {
    'sampling_rate': 16000,
    'frame_length_in_s': 0.04,
    'frame_step_in_s': 0.02,
    'num_mel_bins': 40,
    'lower_frequency': 20,
    'upper_frequency': 4000,
    'num_coefficients': 10
}

class Normalization():
    def __init__(self, bit_depth):
        self.max_range = bit_depth.max

    def normalize_audio(self, audio):
        audio_float32 = tf.cast(audio, tf.float32)
        audio_normalized = audio_float32 / self.max_range

        return audio_normalized

    def normalize(self, audio, label):
        audio_normalized = self.normalize_audio(audio)

        return audio_normalized, label


class Spectrogram():
    def __init__(self, sampling_rate, frame_length_in_s, frame_step_in_s):
        self.frame_length = int(frame_length_in_s * sampling_rate)
        self.frame_step = int(frame_step_in_s * sampling_rate)

    def get_spectrogram(self, audio):
        stft = tf.signal.stft(
            audio,
            frame_length=self.frame_length,
            frame_step=self.frame_step,
            fft_length=self.frame_length
        )
        spectrogram = tf.abs(stft)

        return spectrogram

    def get_spectrogram_and_label(self, audio, label):
        spectrogram = self.get_spectrogram(audio)

        return spectrogram, label

class VAD():
    def __init__(
        self,
        sampling_rate,
        frame_length_in_s,
        frame_step_in_s,
        dBthres,
        duration_thres,
    ):
        self.frame_length_in_s = frame_length_in_s
        self.frame_step_in_s = frame_step_in_s
        self.spec_processor = Spectrogram(
            sampling_rate, frame_length_in_s, frame_step_in_s,
        )
        self.dBthres = dBthres
        self.duration_thres = duration_thres

    def is_silence(self, audio):
        spectrogram = self.spec_processor.get_spectrogram(audio)

        dB = 20 * tf.math.log(spectrogram + 1.e-6)
        energy = tf.math.reduce_mean(dB, axis=1)
        min_energy = tf.reduce_min(energy)

        rel_energy = energy - min_energy
        non_silence = rel_energy > self.dBthres
        non_silence_frames = tf.math.reduce_sum(tf.cast(non_silence, tf.float32))
        non_silence_duration = self.frame_length_in_s + self.frame_step_in_s * (non_silence_frames - 1)

        if non_silence_duration > self.duration_thres:
            return 0
        else:
            return 1

class MelSpectrogram():
    def __init__(
        self,
        sampling_rate,
        frame_length_in_s,
        frame_step_in_s,
        num_mel_bins,
        lower_frequency,
        upper_frequency
    ):
        self.spectrogram_processor = Spectrogram(sampling_rate, frame_length_in_s, frame_step_in_s)
        num_spectrogram_bins = self.spectrogram_processor.frame_length // 2 + 1

        self.linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
            num_mel_bins=num_mel_bins,
            num_spectrogram_bins=num_spectrogram_bins,
            sample_rate=sampling_rate,
            lower_edge_hertz=lower_frequency,
            upper_edge_hertz=upper_frequency
        )

    def get_mel_spec(self, audio):
        spectrogram = self.spectrogram_processor.get_spectrogram(audio)
        mel_spectrogram = tf.matmul(spectrogram, self.linear_to_mel_weight_matrix)
        log_mel_spectrogram = tf.math.log(mel_spectrogram + 1.e-6)

        return log_mel_spectrogram

    def get_mel_spec_and_label(self, audio, label):
        log_mel_spectrogram = self.get_mel_spec(audio)

        return log_mel_spectrogram, label

class MFCC():
    def __init__(
        self,
        sampling_rate,
        frame_length_in_s,
        frame_step_in_s,
        num_mel_bins,
        lower_frequency,
        upper_frequency,
        num_coefficients
    ):
        self.mel_spec_processor = MelSpectrogram(
            sampling_rate, frame_length_in_s, frame_step_in_s, num_mel_bins, lower_frequency, upper_frequency
        )
        self.num_coefficients = num_coefficients

    def get_mfccs(self, audio):
        log_mel_spectrogram = self.mel_spec_processor.get_mel_spec(audio)
        mfccs = tf.signal.mfccs_from_log_mel_spectrograms(log_mel_spectrogram)
        mfccs = mfccs[..., :self.num_coefficients]

        return mfccs

    def get_mfccs_and_label(self, audio, label):
        mfccs = self.get_mfccs(audio)

        return mfccs, label

vad_processor = VAD(vad_sample_rate, 0.032, 0.5 * 0.032, 10, 0.1)
normalization = Normalization(tf.int16)
mfcc_processor = MFCC(**PREPROCESSING_ARGS)

interpreter = tf.lite.Interpreter(model_path='./model11.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

LABELS = ['down', 'up']

def predict(audio_tensor):
    data = mfcc_processor.get_mfccs(audio_tensor)

    data = tf.expand_dims(data, 0)
    data = tf.expand_dims(data, -1)

    interpreter.set_tensor(input_details[0]['index'], data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    top_index = np.argmax(output[0])
    predicted_label = LABELS[top_index]

    return predicted_label, output[0][top_index]

measuring = False

def measurement_loop():
    # collect data every 2 seconds
    global measuring
    while True:
        if measuring:
            timestamp = int(time.time() * 1000)

            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                redis_client.ts().add(temperature_key, timestamp, temperature)
                redis_client.ts().add(humidity_key, timestamp, humidity)

            except:
                print('sensor failure')
                dht_device.exit()

            time.sleep(2)

def callback(indata, frames, callback_time, status):
    global measuring

    audio = tf.cast(indata, tf.float32)
    audio = signal.resample_poly(audio, up=1, down=int(recording_samplerate / vad_sample_rate))
    audio = tf.convert_to_tensor(audio)
    audio = tf.squeeze(audio)
    audio = normalization.normalize_audio(audio)

    is_silence = vad_processor.is_silence(audio)
    if not is_silence:
        prediction, probability = predict(audio)
        if probability > 0.99:
            if prediction == 'up':
                measuring = True
            elif prediction == 'down':
                measuring = False


with sd.InputStream(samplerate=recording_samplerate, channels=1, dtype='int16', callback=callback, blocksize=recording_samplerate):
    measurement_thread = Thread(target=measurement_loop)
    measurement_thread.start()
    while True:
        continue

