from aviator_ai_model import AviatorAIPredictor
import matplotlib.pyplot as plt

# Initialize
ai = AviatorAIPredictor(sequence_length=10)

# Generate and preprocess data
ai.generate_data(size=10000)
X, y = ai.preprocess()

# Train the model
ai.train(X, y, epochs=5)

# Predict last 100 multipliers
predicted = ai.predict(X[-100:])
actual = ai.df["multiplier"].values[-100:]

# Plot prediction vs actual
plt.plot(actual[-100:], label="Actual")
plt.plot(predicted.flatten(), label="Predicted")
plt.title("Aviator AI Prediction (LSTM)")
plt.legend()
plt.grid(True)
plt.show()
