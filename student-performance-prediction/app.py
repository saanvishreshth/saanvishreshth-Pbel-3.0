# app.py
# Main Flask application file.
# This handles all the routes for the Student Performance Prediction System.

from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
from datetime import datetime
import csv
import io

from model import predict_score, get_category, get_suggestions

app = Flask(__name__)

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Creates the predictions table if it doesn't already exist."""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            study_hours REAL,
            attendance REAL,
            previous_marks REAL,
            assignments INTEGER,
            participation INTEGER,
            sleep_hours REAL,
            internet_study REAL,
            predicted_score REAL,
            performance TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# Run this once when the app starts
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Get all form values
        student_name = request.form.get("student_name")
        study_hours = float(request.form.get("study_hours"))
        attendance = float(request.form.get("attendance"))
        previous_marks = float(request.form.get("previous_marks"))
        assignments = int(request.form.get("assignments"))
        participation = int(request.form.get("participation"))
        sleep_hours = float(request.form.get("sleep_hours"))
        internet_study = float(request.form.get("internet_study"))

        # Get prediction from our model helper
        score = predict_score(
            study_hours, attendance, previous_marks,
            assignments, participation, sleep_hours, internet_study
        )
        category = get_category(score)
        suggestions = get_suggestions(
            study_hours, attendance, assignments, participation, category
        )

        # Save this prediction into the database
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO predictions
            (student_name, study_hours, attendance, previous_marks, assignments,
             participation, sleep_hours, internet_study, predicted_score, performance, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_name, study_hours, attendance, previous_marks, assignments,
            participation, sleep_hours, internet_study, score, category,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        conn.commit()
        conn.close()

        # Send data to the result page
        return render_template(
            "result.html",
            name=student_name,
            score=score,
            category=category,
            suggestions=suggestions
        )

    # If it's a GET request, just show the empty form
    return render_template("predict.html")


@app.route("/history")
def history():
    conn = get_db_connection()

    # Handle search
    search_query = request.args.get("search", "")
    # Handle sorting
    sort_by = request.args.get("sort", "created_at")

    allowed_sort_columns = ["student_name", "predicted_score", "created_at", "performance"]
    if sort_by not in allowed_sort_columns:
        sort_by = "created_at"

    if search_query:
        records = conn.execute(
            f"SELECT * FROM predictions WHERE student_name LIKE ? ORDER BY {sort_by} DESC",
            ("%" + search_query + "%",)
        ).fetchall()
    else:
        records = conn.execute(
            f"SELECT * FROM predictions ORDER BY {sort_by} DESC"
        ).fetchall()

    # Simple stats for the stat cards
    all_scores = conn.execute("SELECT predicted_score FROM predictions").fetchall()
    conn.close()

    total_predictions = len(all_scores)
    if total_predictions > 0:
        avg_score = round(sum(row["predicted_score"] for row in all_scores) / total_predictions, 1)
        highest_score = max(row["predicted_score"] for row in all_scores)
    else:
        avg_score = 0
        highest_score = 0

    return render_template(
        "history.html",
        records=records,
        total_predictions=total_predictions,
        avg_score=avg_score,
        highest_score=highest_score,
        search_query=search_query
    )


@app.route("/delete/<int:record_id>")
def delete(record_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM predictions WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("history"))


@app.route("/export-csv")
def export_csv():
    """Lets the user download all history records as a CSV file."""
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM predictions ORDER BY created_at DESC").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Student Name", "Study Hours", "Attendance", "Previous Marks",
        "Assignments", "Participation", "Sleep Hours", "Internet Study",
        "Predicted Score", "Performance", "Date"
    ])

    for row in records:
        writer.writerow([
            row["student_name"], row["study_hours"], row["attendance"],
            row["previous_marks"], row["assignments"], row["participation"],
            row["sleep_hours"], row["internet_study"], row["predicted_score"],
            row["performance"], row["created_at"]
        ])

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=prediction_history.csv"
    return response


if __name__ == "__main__":
    app.run(debug=True)
