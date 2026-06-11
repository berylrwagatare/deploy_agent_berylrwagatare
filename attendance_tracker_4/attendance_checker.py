import json
import csv
import os
from datetime import datetime

CONFIG_PATH  = os.path.join("Helpers", "config.json")
ASSETS_PATH  = os.path.join("Helpers", "assets.csv")
REPORTS_PATH = os.path.join("reports", "reports.log")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def load_students():
    students = []
    with open(ASSETS_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    return students

def calculate_attendance(student):
    attended  = int(student.get("classes_attended", 0))
    total     = int(student.get("total_classes", 1))
    return round((attended / total) * 100, 2) if total > 0 else 0.0

def classify(percentage, thresholds):
    if percentage >= thresholds["warning"]:
        return "Good Standing"
    elif percentage >= thresholds["failure"]:
        return "Warning"
    else:
        return "Failure"

def generate_report():
    config     = load_config()
    thresholds = config.get("thresholds", {"warning": 75, "failure": 50})
    students   = load_students()

    lines = [f"Attendance Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "=" * 50]

    for s in students:
        pct    = calculate_attendance(s)
        status = classify(pct, thresholds)
        lines.append(f"{s['name']:25s} | {pct:6.2f}% | {status}")

    lines.append("=" * 50)
    report_text = "\n".join(lines)
    print(report_text)

    os.makedirs("reports", exist_ok=True)
    with open(REPORTS_PATH, "a") as f:
        f.write(report_text + "\n\n")
    print(f"\n[INFO] Report appended to {REPORTS_PATH}")

if __name__ == "__main__":
    generate_report()
