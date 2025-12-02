import uuid
import time
from datetime import datetime
import sounddevice as sd
import numpy as np
from threading import Thread
import tensorflow as tf
import adafruit_dht
from board import D4
from scipy import signal
 

mac_address = hex(uuid.getnode())
dht_device = adafruit_dht.DHT11(D4)
recording_samplerate = 48000
vad_sample_rate = 16000
t = 1


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


vad_processor = VAD(vad_sample_rate, 0.032, 0.5 * 0.032, 10, 0.1)
normalization = Normalization(tf.int16)

measuring = False
last_change_ts = 0

def measurement_loop():
    global measuring
    while True:
        if measuring:
            timestamp = int(time.time() * 1000)
            formatted_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')

            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                print(f'{formatted_time} - {mac_address}:temperature = {temperature}')
                print(f'{formatted_time} - {mac_address}:humidity = {humidity}')
            
            except:
                print('sensor failure')
                dht_device.exit()

            time.sleep(2)



def callback(indata, frames, callback_time, status):
    global measuring, last_change_ts
    
    audio = tf.cast(indata, tf.float32)
    audio = signal.resample_poly(audio, up=1, down=int(recording_samplerate / vad_sample_rate))
    audio = tf.convert_to_tensor(audio)
    audio = tf.squeeze(audio)
    audio = normalization.normalize_audio(audio)
    
    is_silence = vad_processor.is_silence(audio)
    current_ts = time.time()
    if (not is_silence) and (current_ts - last_change_ts) >= 5:
        measuring = not measuring
        last_change_ts = current_ts
        

with sd.InputStream(samplerate=recording_samplerate, channels=1, dtype='int16', callback=callback, blocksize=recording_samplerate*t):
    measurement_thread = Thread(target=measurement_loop)
    measurement_thread.start()
    while True:
        continue
