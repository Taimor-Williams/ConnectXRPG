import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Load your dataset using the appropriate file path or URL
df = pd.read_csv('Game.csv')  # Update 'your_dataset.csv' with the correct file path or URL

# Assuming you have a feature matrix X and a target variable y
X = df[['Moves', 'feature2', ...]]  # Replace 'feature1', 'feature2', ... with your actual feature names
y = df['number_of_moves_left']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# Print the evaluation metrics
print('R-squared (R2):', r2)
print('Mean Squared Error (MSE):', mse)