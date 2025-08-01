import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class AviatorAIPredictor:
    def __init__(self, sequence_length=10):
        self.sequence_length = sequence_length
        self.model = self._build_model()
        self.scaler = MinMaxScaler()

    def generate_data(self, size=10000, seed=42):
        np.random.seed(seed)
        def generate_multiplier():
            r = np.random.random()
            if r < 0.01:
                return 1.00
            return round(np.floor(100 * (1 / (1 - r))) / 100, 2)

        data = [generate_multiplier() for _ in range(size)]
        self.df = pd.DataFrame(data, columns=["multiplier"])
        return self.df

    def preprocess(self):
        scaled = self.scaler.fit_transform(self.df)
        X, y = [], []
        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i+self.sequence_length])
            y.append(scaled[i+self.sequence_length])
        return np.array(X), np.array(y)

    def _build_model(self):
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(self.sequence_length, 1)),
            LSTM(32),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, X, y, epochs=10, batch_size=64):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    def predict(self, X_input):
        prediction = self.model.predict(X_input, verbose=0)
        return self.scaler.inverse_transform(prediction)
