# AI-Driven Student Performance Prediction System

A mini-project that predicts a student's expected final exam score using a simple
Machine Learning model, built with Python, Flask, and a bit of vanilla JavaScript.

## Project Introduction

This project was made to explore how machine learning can be used to predict student
performance based on daily habits like study hours, attendance, and sleep. It uses a
Linear Regression model trained on a generated dataset of 500 student records, and
wraps it in a simple Flask web app so anyone can enter their details and get an
instant prediction.

## Features

- Predicts a student's final score based on 7 input factors
- Classifies performance into 4 categories: Excellent, Good, Average, Needs Improvement
- Gives personalized suggestions for improvement
- Saves every prediction to a local SQLite database
- History page with search, sort, and delete options
- Export prediction history to CSV
- Statistics cards (Total Predictions, Average Score, Highest Score)
- Charts (bar chart + pie chart) using Chart.js
- Dark mode toggle
- Loading spinner while predicting
- Download result as PDF (via browser print)
- Client-side form validation

## Technologies Used

**Frontend:** HTML, CSS, Vanilla JavaScript, Chart.js
**Backend:** Python, Flask
**Machine Learning:** Pandas, NumPy, Scikit-learn
**Database:** SQLite

## Folder Structure

```
project/
│
├── app.py                  # Main Flask app (routes)
├── model.py                 # Prediction + suggestion helper functions
├── train_model.py           # Script to train and save the ML model
├── generate_dataset.py      # Script used to generate the CSV dataset
├── student_performance.csv  # Training data (500 student records)
├── model.pkl                 # Saved trained model
├── database.db               # SQLite database (created automatically)
│
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   └── history.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

## Installation Steps

1. Make sure Python 3.8+ is installed.
2. Clone or download this project folder.
3. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
4. Install the required packages:
   ```
   pip install flask pandas numpy scikit-learn
   ```

## How to Train the Model

The model is already trained and saved as `model.pkl`, but if you want to
regenerate the dataset or retrain it yourself:

1. Generate a fresh dataset (optional):
   ```
   python generate_dataset.py
   ```
2. Train the model:
   ```
   python train_model.py
   ```
   This will print the model's accuracy (MAE and R2 score) and save `model.pkl`.

## How to Run Flask

1. Make sure `model.pkl` exists (run the training step above if it doesn't).
2. Start the Flask server:
   ```
   python app.py
   ```
3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Screenshots

_(Add your screenshots here once you run the project)_

- Home Page: `screenshots/home.png`
- Predict Page: `screenshots/predict.png`
- Result Page: `screenshots/result.png`
- History Page: `screenshots/history.png`

## Future Improvements

- Add user login so each student can view only their own history
- Try other models like Random Forest and compare accuracy
- Add more input features (e.g. extracurricular activities)
- Deploy the app online (Render / Railway / PythonAnywhere)
- Add email notifications with the prediction result
