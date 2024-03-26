# Job Application Tracker CLI Application

## Overview
The Job Application Tracker CLI application is designed to help users manage their job search process efficiently. The application allows users to track job applications, companies, contacts, and related information, providing a centralized platform for organizing and managing job search activities.

## Problem Statement
In today's competitive job market, managing multiple job applications, deadlines, and interview schedules can be challenging for job seekers. The Job Application Tracker CLI application aims to solve this problem by providing a centralized platform for users to track job applications, companies, and contacts. By using this application, job seekers can stay organized, manage their job search efficiently, and increase their chances of success in finding suitable employment opportunities.

## Features
- Add new companies, contacts, and job applications to the database.
- View a list of all companies, contacts, and job applications.
- Delete companies, contacts, and job applications from the database.
- View jobs related to a specific company.
- View contacts related to a specific company.

## Technology Stack
- Python 3
- SQLAlchemy
- Click (for CLI interface)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bradleymbuvi/Job-Application-Tracker

2. Install dependencies:

3. Run pipenv install to create a virtual environment and install required Dependencies
4. Run pipenv shell to activate the virtual environment.
5. Start the application by executing python job_tracker.py

## CLI Commands

- create _company: Create a new company.
- list_companies: List all companies.
- delete_company: Delete a company.
- view_company_jobs: View jobs related to a company.
- add_job: Add a new job application to the database with company details, title, description, and application date.
- update_status: Update the application status (e.g., Applied, Interview Scheduled, Rejected, Offer Received) for a specific job.
- search: Search for jobs by company name, title, or keywords.


## Future Enhancements
- Add search functionality to search for specific companies, contacts, or job applications.
- Implement filters to sort and categorize job applications based on status, deadlines, etc.
- Add reminders and notifications for upcoming interviews and application deadlines.
- Integration with external job boards or platforms


Trello Board - https://trello.com/b/1TFi8veO/job-application-tracker