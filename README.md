# Smart Campus Event Management System (SCEMS)

A simple command-line system for campus events, built to demonstrate
Software Configuration Management (Git/GitHub, Jira, Jenkins, Google Sheets/Drive).

## Functionalities
1. **Event Scheduling** (CI-04) - create events, block venue/time clashes
2. **Registration** (CI-03) - student ID validation, seat limits, duplicate and time-clash checks
3. **Notification** (CI-05) - registration confirmations and reminders
4. **Attendance & Certificate** (CI-06) - mark attendance, generate certificates

## Run
    python main.py

## Test
    pip install -r requirements.txt
    python -m pytest

## Project structure
    scems/          source code modules (one file per CI)
    tests/          test cases (CI-09)
    database/       schema script (CI-07)
    Jenkinsfile     build and deployment pipeline (CI-10)
    main.py         command-line interface

## SCM conventions
- Commit message: `SCEMS-<jira number> [CI-<id>] <short description>`
- Branch name: `feature/SCEMS-<n>-<name>` or `bugfix/SCEMS-<n>-<name>`
- Release tags: `vMAJOR.MINOR.PATCH` (e.g. v1.0.0)
- Every change is raised as a Jira issue and merged through a GitHub pull request
