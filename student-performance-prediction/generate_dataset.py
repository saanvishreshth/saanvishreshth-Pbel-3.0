# generate_dataset.py
# Small helper script I wrote to create fake but realistic student data
# to train the prediction model. I only had to run this once.

import numpy as np
import pandas as pd

# using a fixed seed so the data is the same every time I run this
np.random.seed(42)

NUM_STUDENTS = 500

def make_data():
    study_hours = np.round(np.random.uniform(0.5, 10, NUM_STUDENTS), 1)
    attendance = np.round(np.random.uniform(40, 100, NUM_STUDENTS), 1)
    previous_marks = np.round(np.random.uniform(30, 100, NUM_STUDENTS), 1)
    assignments = np.random.randint(0, 11, NUM_STUDENTS)  # out of 10
    participation = np.random.randint(1, 6, NUM_STUDENTS)  # scale 1-5
    sleep_hours = np.round(np.random.uniform(4, 9, NUM_STUDENTS), 1)
    internet_study = np.round(np.random.uniform(0, 5, NUM_STUDENTS), 1)

    # Making the final score depend on the above in a way that
    # roughly makes sense (more study/attendance -> higher score)
    final_score = (
        study_hours * 3.5
        + attendance * 0.35
        + previous_marks * 0.25
        + assignments * 1.8
        + participation * 2.0
        + sleep_hours * 1.0
        + internet_study * 1.2
        - 15  # base offset so numbers land in a normal range
    )

    # add a bit of random noise so it isn't a perfect formula
    noise = np.random.normal(0, 5, NUM_STUDENTS)
    final_score = final_score + noise

    # clip so scores stay between 0 and 100
    final_score = np.clip(final_score, 0, 100)
    final_score = np.round(final_score, 1)

    df = pd.DataFrame({
        "StudyHours": study_hours,
        "Attendance": attendance,
        "PreviousMarks": previous_marks,
        "Assignments": assignments,
        "Participation": participation,
        "SleepHours": sleep_hours,
        "InternetStudy": internet_study,
        "FinalScore": final_score
    })

    return df


if __name__ == "__main__":
    data = make_data()
    data.to_csv("student_performance.csv", index=False)
    print("Dataset created: student_performance.csv")
    print(data.head())
