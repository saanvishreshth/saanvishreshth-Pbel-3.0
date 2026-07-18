# train_model.py
# This script trains our prediction model on the student CSV data
# and saves it to a file (model.pkl) so app.py can load it later.
# I just run this once whenever I update the dataset.

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# 1. Load the dataset
data = pd.read_csv("student_performance.csv")

# 2. Split into input features (X) and the thing we want to predict (y)
feature_columns = [
    "StudyHours",
    "Attendance",
    "PreviousMarks",
    "Assignments",
    "Participation",
    "SleepHours",
    "InternetStudy"
]

X = data[feature_columns]
y = data["FinalScore"]

# 3. Split data into training set and testing set (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Create and train the model
# Using simple Linear Regression since it's easy to understand
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Check how good the model is on the test data
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model training complete!")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")

# 6. Save the trained model to a file using pickle
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as model.pkl")
