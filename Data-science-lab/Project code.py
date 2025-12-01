#importing libraries
import numpy as np
import pandas as pd
import librosa
import noisereduce as nr
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
from imblearn.over_sampling import RandomOverSampler
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, accuracy_score

#reading file
development = pd.read_csv('data/development.csv')
audio_path=development.iloc[:, 1].values
labels=development.iloc[:, -1].values


#plotting durations of audio files
durations=[]
for i in audio_path:
    audio_p, sample_rate = librosa.load(i, sr=16000)
    D=librosa.get_duration(y=audio_p, sr=16000)
    durations.append(D)

plt.hist(durations, bins=50)
plt.xlabel('Duration (seconds)')
plt.ylabel('Number of audio files')
plt.title('Distribution of audio file durations')
plt.show()


#plotting one audio before and after trimming and reducing noise
one_audio, sr = librosa.load(audio_path[0], sr=16000)
audio_trimmed_o=librosa.effects.trim(one_audio,top_db=15)
audio_reduced_o = nr.reduce_noise(audio_trimmed_o[0], sr)

pd.Series(one_audio).plot(figsize=(10,5),lw=1,title='one audio example')
plt.show()

pd.Series(audio_reduced_o).plot(figsize=(10,5),lw=1,title='one audio example after trim and reduce noise')
plt.show()



#doing some preprocessing
def features_extractor(file):
    #load the file (audio)
    audio, sample_rate = librosa.load(file, sr=16000)
    #timming audio
    audio_trimmed=librosa.effects.trim(audio,top_db=15)
    # reducing noise
    audio_reduced = nr.reduce_noise(audio_trimmed[0], sample_rate)
    # padding
    p=230000-len(audio_reduced)
    pad=np.pad(audio_reduced,(0,p))
    #MFCCS
    mfccs = librosa.feature.mfcc(y=pad, sr=sample_rate)
    return mfccs


# Now we iterate through every audio file and extract features 
# using Mel-Frequency Cepstral Coefficients
extracted_features=[]
for index_num,row in tqdm(development.iterrows()):
    file_name = audio_path[index_num]
    data=features_extractor(file_name)
    extracted_features.append(data)

X=np.array(extracted_features)
y=labels
X = X.reshape(X.shape[0], -1)


#over_sampling data
rus = RandomOverSampler(random_state=0)
X_resampled, y_resampled = rus.fit_resample(X, y)

#encoding labels
labelencoder=LabelEncoder()
y_resampled=to_categorical(labelencoder.fit_transform(y_resampled))


# Train Test Split
X_resampled_train,X_resampled_test,y_resampled_train,y_resampled_test=train_test_split(X_resampled,y_resampled,test_size=0.15,random_state=0)


#scaling data with MinMaxScaler
scaler = MinMaxScaler()
X_resampled_train = scaler.fit_transform(X_resampled_train)
X_resampled_test = scaler.transform(X_resampled_test)



#PCA
pca = PCA(n_components = 0.95)
X_resampled_train = pca.fit_transform(X_resampled_train)
X_resampled_test = pca.transform(X_resampled_test)




#training model
ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=1024, activation='relu'))
ann.add(tf.keras.layers.Dropout(0.2)) # adding dropout
ann.add(tf.keras.layers.Dense(units=512, activation='relu'))
ann.add(tf.keras.layers.Dropout(0.2)) # adding dropout
ann.add(tf.keras.layers.Dense(units=256, activation='relu'))
ann.add(tf.keras.layers.Dropout(0.2)) # adding dropout
ann.add(tf.keras.layers.Dense(units=128, activation='relu'))
ann.add(tf.keras.layers.Dropout(0.2)) # adding dropout
ann.add(tf.keras.layers.Dense(units=64, activation='relu'))

# Adding the output layer
ann.add(tf.keras.layers.Dense(units=7, activation='sigmoid'))

# Compiling the ANN
ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Training the ANN on the Training set
H = ann.fit(X_resampled_train, y_resampled_train, epochs=100, batch_size=64, validation_data=(X_resampled_test, y_resampled_test))

#predicting test data
y_pred = ann.predict(X_resampled_test)


#plotting accuracy and loss of model
plt.plot(H.history['accuracy'])
plt.plot(H.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(H.history['loss'])
plt.plot(H.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()



# confusion_matrix
y_resampled_test_pp = labelencoder.inverse_transform(np.argmax(y_resampled_test, axis=1))
y_pred_pp = labelencoder.inverse_transform(np.argmax(y_pred, axis=1))

cm = confusion_matrix(y_resampled_test_pp, y_pred_pp)
print(cm)
print(accuracy_score(y_resampled_test_pp, y_pred_pp))


#plotting 
sns.heatmap(cm, annot=True, fmt='d',cmap="YlGnBu")
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.title('Confusion matrix')
plt.show()
# predicting new data

predict=[]
evaluation = pd.read_csv('data/evaluation.csv')
path=evaluation.iloc[:,1].values
Id=evaluation.iloc[:,0].values

def features_extractor_p(file_p):
    #load the file (audio)
    audio_p, sample_rate_p = librosa.load(file_p, sr=16000)
    # audio_resampled_p = librosa.resample(audio_p, sample_rate_p, 8000)
    audio_trimmed_p=librosa.effects.trim(audio_p,top_db=15)
    y_reduced_p = nr.reduce_noise(audio_trimmed_p[0], sample_rate_p)
    p_p=230000-len(y_reduced_p)
    pad_p=np.pad(y_reduced_p,(0,p_p))
    mfccs_p = librosa.feature.mfcc(y=pad_p, sr=sample_rate_p)
    return mfccs_p

### Now we iterate through every audio file and extract features 
### using Mel-Frequency Cepstral Coefficients
extracted_features_p=[]
for index_num,row in tqdm(evaluation.iterrows()):
    file_name_p = path[index_num]
    data_p=features_extractor_p(file_name_p)
    extracted_features_p.append(data_p)

X_p=np.array(extracted_features_p)
X_p= X_p.reshape(X_p.shape[0], -1)


X_p = scaler.transform(X_p) 

X_p= pca.transform(X_p)  

y_p = ann.predict(X_p)

y_p = labelencoder.inverse_transform(np.argmax(y_p, axis=1))



Testing_evaluation=[]
Testing_evaluation.append([Id,y_p])

df = pd.DataFrame({'Id': Id, 'Predicted': y_p})

df.to_csv('ANN.csv', index=False)



















