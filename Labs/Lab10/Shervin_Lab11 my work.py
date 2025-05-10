import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Load the dataset
df = pd.read_csv('./Lab_11_dataset/student_depression_dataset.csv')
print('Data Loaded Successfully!')
print(df.head())

# Dataset Overview
print(df.info())
print(df.describe())

# Handling Missing Data
missing_values = df.isnull().sum()
print('Missing Values in Each Column:')
print(missing_values[missing_values > 0])

# Fill missing values
df.fillna(method='ffill', inplace=True)
print('Missing values filled where needed.')

# Encoding Categorical Data
df = pd.get_dummies(df, columns=[
    'Gender', 'City', 'Profession', 'Degree', 'Dietary Habits',
    'Have you ever had suicidal thoughts ?',
    'Financial Stress', 'Family History of Mental Illness'
], drop_first=True)
print('Data successfully encoded.')

# Data Visualization
df.hist(figsize=(15, 10), bins=20)
plt.show()

sns.countplot(x='Depression', data=df)
plt.show()

plt.figure(figsize=(15, 10))
sns.heatmap(df.corr(), annot=False, cmap='coolwarm')
plt.show()

sns.boxplot(x='Depression', y='CGPA', data=df)
plt.show()

# Part 2: Modeling with DecisionTreeRegressor
X = df.drop(columns=['Depression'])
y = df['Depression']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("R² Score:", r2_score(y_test, y_pred))
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
