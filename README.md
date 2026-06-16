# Attendance Tracker – Project Bootstrapper
## WALKTHROUGH VIDEO 
https://youtu.be/XZktAk7xeK4
## Overview 
`setup_project.sh` is a shell script that automates the complete setup of the **Student Attendance Tracker** workspace. It handles directory creation, file generation, dynamic configuration via `sed`, environment validation, and graceful cleanup on user interruption.

---

## Prerequisites
| Requirement | Notes |
|---|---|
| Bash 3.2+ | Pre-installed on macOS and all Linux distros |
| python3 | Optional at setup time, required to run the tracker |

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/berylrwagatare/deploy_agent_berylrwagatare.git
cd deploy_agent_berylrwagatare
```

### 2. Make the script executable
```bash
chmod +x setup_project.sh
```

### 3. Run the script
```bash
./setup_project.sh

./setup_project.sh cohort_2025
```

### 4. Follow the prompts
The script will ask you:
1. **Project identifier** (if not passed as an argument) → creates `attendance_tracker_<identifier>/`
2. **Update thresholds?** → enter new Warning and Failure percentages (integers 1–100), or press Enter to keep defaults

### 5. Run the attendance tracker
```bash
cd attendance_tracker_<identifier>
python3 attendance_checker.py
```
The report is printed to the terminal and appended to `reports/reports.log`.

---

## Project Structure Created
```
attendance_tracker_{input}/
├── attendance_checker.py   ← Main application logic
├── Helpers/
│   ├── assets.csv          ← Student attendance data
│   └── config.json         ← Threshold configuration
└── reports/
    └── reports.log         ← Cumulative report log
```

---

## Triggering the Archive / Cleanup Feature
The script installs a **SIGINT trap** (Ctrl + C). To trigger it:

1. Start the script normally:
   ```bash
   ./setup_project.sh demo
   ```
2. At **any point** during execution, press **Ctrl + C**.
3. The trap fires and:
   - **Archives** the current (possibly incomplete) project directory into `attendance_tracker_demo_archive.tar.gz`
   - **Deletes** the incomplete `attendance_tracker_demo/` directory
   - Prints a confirmation and exits

This keeps your workspace clean even after a cancelled run.

---

## Configuration Details (`config.json`)
```json
{
  "thresholds": {
    "warning": 75,
    "failure": 50
  },
  "institution": "ALU",
  "academic_year": "2025-2026"
}
```
`sed` performs an **in-place edit** of these two numeric values when you choose to update thresholds. Input is validated to be a whole number between 1 and 100 before `sed` is called.

---

## Error Handling
| Scenario | Behaviour |
|---|---|
| Empty project identifier | Script exits with an error message |
| Directory already exists | Prompts to overwrite; aborts if user declines |
| Non-numeric threshold input | Re-prompts until valid input is given |
| Directory creation fails | Exits with a permissions error |
| python3 not found | Prints a warning; setup still completes |
| SIGINT (Ctrl+C) | Archives + removes partial directory, then exits |

---

## License
MIT – see repository root.
