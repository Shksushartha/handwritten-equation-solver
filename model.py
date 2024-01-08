from keras.models import load_model
import cv2
import os
import numpy as np
from keras import backend as K
from keras.models import Sequential
from keras.layers import Input, Dropout, Flatten, Conv2D, MaxPooling2D, Dense, Activation
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping
# from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

def mathsymbol():
    model = Sequential()
    model.add(Conv2D(32, (5, 5), input_shape=(45, 45, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    # model.add(Dense(28, activation='softmax'))
    model.add(Dense(26, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def predict_image(img):
    K.clear_session()
    model = mathsymbol()
    model.load_weights('HESWeightsFinal.h5')
    # model.load_weights('weights.h5')
    ret, thresholded_img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    img = cv2.resize(thresholded_img, (45, 45))
    img = np.reshape(img, (1, 45, 45, 3))
    prediction = model.predict(img)
    L = ['(', ')', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'a', 'b', 'c', 'e', 'c', 'e', 'k', 'j', 'x', 'y', 'x', 'y', 'z']
    # L = ['(', ')', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '2', '2', '6', 'beta', '(', 'e',
    #      'i', 'j', 'k', 'pi', 'x', 'x', '2']
    ans = L[np.argmax(prediction)]

    return ans