import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


digits = load_digits()
X = digits.data
y = digits.target
y = np.eye(10)[y]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
input_size = X_train.shape[1]
hidden_size = 128
output_size = 10
weights_input_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
weights_hidden_output = np.random.uniform(-1, 1, (hidden_size, output_size))
learning_rate = 0.1
epochs = 1000
for epoch in range(epochs):
    for i in range(len(X_train)):
        input_layer = X_train[i].reshape(1, -1)
        hidden_layer = sigmoid(np.dot(input_layer, weights_input_hidden))
        output_layer = sigmoid(np.dot(hidden_layer, weights_hidden_output))
        output_error = y_train[i].reshape(1, -1) - output_layer
        output_delta = output_error * sigmoid_derivative(output_layer)
        hidden_error = output_delta.dot(weights_hidden_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(hidden_layer)
        weights_hidden_output += learning_rate * hidden_layer.T.dot(output_delta)
        weights_input_hidden += learning_rate * input_layer.T.dot(hidden_delta)
correct = 0
for i in range(len(X_test)):
    input_layer = X_test[i].reshape(1, -1)
    hidden_layer = sigmoid(np.dot(input_layer, weights_input_hidden))
    output_layer = sigmoid(np.dot(hidden_layer, weights_hidden_output))
    predicted = np.argmax(output_layer)
    actual = np.argmax(y_test[i])
    if predicted == actual:
        correct += 1
accuracy = correct / len(X_test)
print(f"测试集准确率: {accuracy * 100:.2f}%")