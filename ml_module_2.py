from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import pandas as pd
import ast
import numpy as np

df = pd.read_csv('MLsavedGames/GamesFile0.csv')
X_train_series = df['BoardState']
X_train_np = X_train_series.to_numpy()
X_train_list = X_train_series.tolist()
print(X_train_list)
#X_train = ast.literal_eval(X_train_str)
# y_train = df['Outcome']
# # Load and preprocess your Connect Four dataset
# model_lr = LogisticRegression()
# model_lr.fit(X_train, y_train)


# # Load and preprocess your Connect Four dataset
# model_gbm = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.001, max_depth=4)
# model_gbm.fit(X_train, y_train)
# print(model_gbm)



