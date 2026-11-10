# NHS Band 5 Healthcare Job Tracking Pipeline

Automated job monitoring system for UK NHS vacancies — focused on entry-level nursing roles.

## Target Roles
- Newly Qualified Nurse
- Pre-registered Nurse  
- New Graduate Nurse
- Band 5 Nurse

## Features
- Scans beta.jobs.nhs.uk across multiple search phrases
- Smart filtering: Excludes Senior, Sister, Matron, Manager, Lead, Consultant, Advanced roles
- Retains Band 5 / Newly Qualified / Graduate / Pre-registered only
- Extracts Job Title, Trust/Employer, Salary, Closing Date, Direct Application Link
- CSV output ready for recruitment reporting

## Workflow
- Weekly automated scans for new vacancies
- CSV database: nhs_nurse_jobs.csv
- Ready for agency tracking and candidate matching

## Tech Stack
Python, Selenium WebDriver, Firefox

## Usage
pip install selenium
python nhs_job_tracker.py

Output: nhs_nurse_jobs.csv
