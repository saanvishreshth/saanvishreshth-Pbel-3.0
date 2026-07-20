# model.py
# Helper functions related to the ML model.
# Keeping this separate from app.py so the Flask file doesn't get messy.

import os
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

with open(MODEL_PATH, "rb") as f:
    trained_model = pickle.load(f)


def predict_score(study_hours, attendance, previous_marks, assignments,
                   participation, sleep_hours, internet_study):
    """
    Takes in the student details and returns a predicted final score.
    """

    # The model expects a DataFrame with the same column names
    # that were used during training.
    input_data = pd.DataFrame([{
        "StudyHours": study_hours,
        "Attendance": attendance,
        "PreviousMarks": previous_marks,
        "Assignments": assignments,
        "Participation": participation,
        "SleepHours": sleep_hours,
        "InternetStudy": internet_study
    }])

    predicted_value = trained_model.predict(input_data)[0]

    # Scores shouldn't be negative or above 100
    if predicted_value < 0:
        predicted_value = 0
    if predicted_value > 100:
        predicted_value = 100

    return round(predicted_value, 1)


def get_category(score):
    """
    Converts a numeric score into a simple performance category.
    """
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Needs Improvement"


def get_suggestions(study_hours, attendance, assignments, participation, category):
    """
    Gives a few basic tips based on the student's inputs.
    This is just simple if-else logic, nothing fancy.
    """
    tips = []

    if study_hours < 4:
        tips.append("Try to increase study hours by 1-2 hours daily.")

    if attendance < 75:
        tips.append("Attend more classes to improve attendance percentage.")

    if assignments < 6:
        tips.append("Improve assignment completion rate.")

    if participation < 3:
        tips.append("Participate more actively in class discussions.")

    if category == "Needs Improvement" or category == "Average":
        tips.append("Practice previous year question papers regularly.")

    # If everything looks fine, still give a small motivational tip
    if len(tips) == 0:
        tips.append("Keep up the great work and maintain this consistency!")

    return tips
