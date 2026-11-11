# NHS Band 5 Job Tracking Pipeline for UK Staffing Agencies

> **For UK Healthcare Recruiters:** Stop checking beta.jobs.nhs.uk manually. This pipeline automates it.

Automated job monitoring system built to help UK staffing agencies track Band 5 nursing vacancies and match candidates faster.

![CSV Output](screenshots/output.png)
*Automated CSV output: Job Title, Trust, Salary, Closing Date, Application Link*

## Why Agencies Use This

**Problem:** Agencies spend 10+ hrs/week manually searching NHS Jobs for newly qualified roles before they close.

**Solution:** Automated weekly scan that delivers ready-to-use CSV for candidate matching.

**Result:** Submit candidates faster, never miss closing dates, save recruiter time.

## Target Roles Tracked

- Newly Qualified Nurse
- Pre-registered Nurse  
- New Graduate Nurse
- Band 5 Nurse / Band 5 Staff Nurse

Smart filter **EXCLUDES**: Senior, Sister, Matron, Manager, Lead, Consultant, Advanced — keeping only entry-level roles agencies need.

## Features

- ✅ Scans beta.jobs.nhs.uk across multiple search phrases
- ✅ Smart filtering for Band 5 only
- ✅ Extracts: Job Title, Trust/Employer, Salary, Closing Date, Direct Application Link
- ✅ CSV output: `nhs_nurse_jobs.csv` — ready for reporting & ATS import
- ✅ Weekly automation ready

![Terminal Run](screenshots/terminal.png)
*Pipeline running — weekly automated scan*

## Output Example

| Job Title | Trust | Salary | Closing Date | Link |
|---|---|---|---|---|
| Band 5 Newly Qualified Nurse | Manchester University NHS | £28k-£34k | 2026-11-20 | jobs.nhs.uk/... |
| Pre-registered Nurse | Leeds Teaching Hospitals | £28k | 2026-11-18 | jobs.nhs.uk/... |

## Tech Stack

Python, Selenium WebDriver, Firefox, CSV

## Quick Start

```bash
pip install selenium
python nhs_job_tracker.py
