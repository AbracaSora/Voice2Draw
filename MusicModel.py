import keras.callbacks
from keras import models, layers, optimizers, regularizers
from keras.utils import plot_model

MusicModel = models.Sequential()
MusicModel.add(layers.Conv1D(256, 5, activation='relu', input_shape=(313, 1)))
MusicModel.add(layers.Conv1D(128, 5, padding='same', activation='relu', kernel_regularizer=regularizers.l2(0.001)))
MusicModel.add(layers.Dropout(0.2))
MusicModel.add(layers.MaxPooling1D(pool_size=8))
MusicModel.add(layers.Conv1D(128, 5, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
MusicModel.add(layers.Dropout(0.2))
MusicModel.add(layers.Conv1D(128, 5, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
MusicModel.add(layers.Dropout(0.2))
MusicModel.add(layers.Conv1D(128, 5, padding='same', activation='relu', kernel_regularizer=regularizers.l2(0.001)))
MusicModel.add(layers.Dropout(0.2))
MusicModel.add(layers.MaxPooling1D(pool_size=3))
MusicModel.add(layers.Conv1D(256, 5, padding='same', activation='relu', kernel_regularizer=regularizers.l2(0.001)))
MusicModel.add(layers.Dropout(0.2))
MusicModel.add(layers.Flatten())
MusicModel.add(layers.Dense(6, activation='softmax'))

MusicModel.summary()