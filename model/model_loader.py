import numpy as np
import mediapipe as mp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

model_catalogue = {
    "qtpn": {
        "path": 'model/holiday/qtpn.h5',
        "no_of_states": 4
    },
    "gptd": {
        "path": 'model/holiday/gptd.h5',
        "no_of_states": 5
    },
    "gpmn": {
        "path": 'model/holiday/gpmn.h5',
        "no_of_states": 5
    }
}

def load_model(model_name: dict):
    """
    Load TensorFlow model of the desired action
    """
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(5,258)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(model_name["no_of_states"], activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    model.load_weights(model_name["path"])

    return model