import numpy as np

subject_list = ["Python", "DBMS", "Networking", "AI"]


def add_totals(data):
    scores = data[subject_list].to_numpy(dtype=float)
    data["Total_Marks"] = scores.sum(axis=1)
    data["Average_Marks"] = np.round(scores.mean(axis=1), 2)
    return data


def get_grade(avg):
    if avg >= 90:
        return "A+"
    if avg >= 80:
        return "A"
    if avg >= 70:
        return "B"
    if avg >= 60:
        return "C"
    if avg >= 50:
        return "D"
    return "F"


def get_result(row):
    all_clear = True
    for sub in subject_list:
        if row[sub] < 40:
            all_clear = False

    if all_clear and row["Attendance"] >= 40:
        return "Pass"
    return "Fail"


def subject_summary(data):
    summary = []

    for sub in subject_list:
        column = data[sub]
        summary.append({
            "Subject": sub,
            "Average_Marks": round(float(np.mean(column.to_numpy())), 2),
            "Highest_Mark": int(column.max()),
            "Lowest_Mark": int(column.min()),
        })

    return summary
