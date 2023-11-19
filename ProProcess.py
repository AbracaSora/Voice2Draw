import pickle
import numpy as np
import keras.callbacks

from keras import optimizers
from keras.utils import to_categorical
from MusicModel import MusicModel

# 读取特征
MFCC = {}
with open('dataset/mfcc_feature_dict.pkl', 'rb') as f:
    MFCC = pickle.load(f)

# 设置标签
emotionDict = {'angry': 0, 'fear': 1, 'happy': 2, 'neutral': 3, 'sad': 4, 'surprise': 5}

data = []
labels = []
data = data + MFCC['angry']
print(len(MFCC['angry']))
for i in range(len(MFCC['angry'])):
    labels.append(0)

data = data + MFCC['fear']
print(len(MFCC['fear']))
for i in range(len(MFCC['fear'])):
    labels.append(1)

print(len(MFCC['happy']))
data = data + MFCC['happy']
for i in range(len(MFCC['happy'])):
    labels.append(2)

print(len(MFCC['neutral']))
data = data + MFCC['neutral']
for i in range(len(MFCC['neutral'])):
    labels.append(3)

print(len(MFCC['sad']))
data = data + MFCC['sad']
for i in range(len(MFCC['sad'])):
    labels.append(4)

print(len(MFCC['surprise']))
data = data + MFCC['surprise']
for i in range(len(MFCC['surprise'])):
    labels.append(5)

print(len(data))
print(len(labels))

# 设置数据维度
data = np.array(data)
data = data.reshape((data.shape[0], data.shape[1], 1))
labels = np.array(labels)
labels = to_categorical(labels)

# 数据标准化
DATA_MEAN = np.mean(data, axis=0)
DATA_STD = np.std(data, axis=0)

data -= DATA_MEAN
data /= DATA_STD

paraDict = {'mean': DATA_MEAN, 'std': DATA_STD, 'emotion': emotionDict}
with open('dataset/mfcc_model_para_dict.pkl', 'wb') as f:
    pickle.dump(paraDict, f)

ratioTrain = 0.8
numTrain = int(data.shape[0] * ratioTrain)
permutation = np.random.permutation(data.shape[0])
data = data[permutation, :]
labels = labels[permutation, :]

x_train = data[:numTrain]
x_val = data[numTrain:]
y_train = labels[:numTrain]
y_val = labels[numTrain:]

print(x_train.shape)
print(y_train.shape)
print(x_val.shape)
print(y_val.shape)

opt = optimizers.legacy.RMSprop(learning_rate=0.0001, decay=1e-6)
MusicModel.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
callbacks_list = [
    keras.callbacks.EarlyStopping(
        monitor='accuracy',
        patience=50,
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='model/speechmfcc_model_checkpoint.h5',
        monitor='val_loss',
        save_best_only=True
    ),
    keras.callbacks.TensorBoard(
        log_dir='speechmfcc_train_log'
    )
]
print(x_train.shape)
history = MusicModel.fit(x_train, y_train,
                         batch_size=16,
                         epochs=200,
                         validation_data=(x_val, y_val),
                         callbacks=callbacks_list)
MusicModel.save('speech_mfcc_model.h5')
MusicModel.save_weights('speech_mfcc_model_weight.h5')
