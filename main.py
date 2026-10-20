import os
import pandas as pd
from functions import add_totals, get_grade, get_result, subject_summary

base_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(base_dir, "students.csv")


def print_title(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run():
    if not os.path.isfile(data_file):
        print("students.csv is missing. Keep it in the same folder as main.py")
        return

    students = pd.read_csv(data_file)
    print_title("STUDENT PERFORMANCE ANALYSIS")
    print("Total students:", students.shape[0])
    print("Columns:", list(students.columns))
    print()
    print(students.head().to_string(index=False))

    students = add_totals(students)
    students["Grade"] = students["Average_Marks"].apply(get_grade)
    students["Result"] = students.apply(get_result, axis=1)

    print_title("STUDENT WISE RESULTS")
    show_cols = ["Student_ID", "Name", "Department", "Total_Marks",
                 "Average_Marks", "Grade", "Attendance", "Result"]
    ranking = students[show_cols].sort_values("Average_Marks", ascending=False)
    print(ranking.to_string(index=False))

    print_title("CLASS SUMMARY")
    best_row = students.loc[students["Average_Marks"].idxmax()]
    worst_row = students.loc[students["Average_Marks"].idxmin()]
    pass_count = len(students[students["Result"] == "Pass"])
    fail_count = len(students) - pass_count

    print("Class average:", round(students["Average_Marks"].mean(), 2))
    print("Highest:", best_row["Name"], "-", round(best_row["Average_Marks"], 2))
    print("Lowest:", worst_row["Name"], "-", round(worst_row["Average_Marks"], 2))
    print("Passed:", pass_count)
    print("Failed:", fail_count)
    print("Pass percentage:", round(pass_count * 100 / len(students), 2), "%")

    print_title("SUBJECT WISE PERFORMANCE")
    subject_table = pd.DataFrame(subject_summary(students))
    print(subject_table.to_string(index=False))
    top_subject = subject_table.loc[subject_table["Average_Marks"].idxmax(), "Subject"]
    print("Best subject (by class average):", top_subject)

    print_title("TOP STUDENTS (average >= 80)")
    top_list = students[students["Average_Marks"] >= 80]
    top_list = top_list.sort_values("Average_Marks", ascending=False)
    if top_list.empty:
        print("Nobody scored 80 or above.")
    else:
        print(top_list[["Student_ID", "Name", "Average_Marks", "Grade"]].to_string(index=False))

    students.to_csv(os.path.join(base_dir, "student_results.csv"), index=False)
    subject_table.to_csv(os.path.join(base_dir, "subject_analysis.csv"), index=False)
    print("\nSaved student_results.csv and subject_analysis.csv")


if __name__ == "__main__":
    run()
