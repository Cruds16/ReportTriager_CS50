# Report Triager

 ![paperplane](/static/images/lietadielko_rm.png)

# Description

## Background

This project was created for the CS50x course by HarvardX. Inspiration for this web application came from my job where I work as a pharmacovigilance specialist.

Pharmacovigilance is a slightly obscure field of pharmaceutical businesses related to drug safety. The main goal of pharmacovigilance is to steadily monitor and evaluate risks and benefits associated with use of medicinal drugs in humans. One of the most significant parts of this work is collection of adverse reactions reports related to use of medicinal products. Reports may be received from various sources, for example from health-care professionals, employees within pharmaceutical companies, but also directly from patients using the drug. Those reports need to be evaluated, tracked and administratively processed in order to allow monitoring of drug safety.

This tool - Report Triager - aims to help workers in pharmacovigilance to track incoming reports and organize their processing within project teams. Data necessary for report evaluation are inserted into Report Triager and can be updated/deleted later, in case of further changes in report evaluation. In addition to storing information about reports, there is a possibility to create and assign relevant to do's with specific deadlines to various team members.

## Features

- registration and log-in of users
- addition of new adverse drug reaction reports to the system
- overview of all tracked reports
- ability to edit/delete report details
- ability to create To do's associated to a particular report - To Do's are assigned to a specified user (team member)
- ability to mark completed, edit or delete individual To Do's
- overview of pending and completed To Do items (personal or all)
- ability to change user password/delete user account

# Technical solutions

- Backend - python, flask
    - Database - SQLite; SQL Alchemy
- Frontend - CSS, HTML, JavaScript with the help of Bootstrap 5.0


# Future possibilities

- "frontend"security - user account confirmation by administrator; confirmation of account via email
- "backend" security - for actual deployment of the application upgrade to other db system would be required
- user allocation to specific projects (separate log-ins)
- addition of visual metrics - graphs to see workload distribution within team; visualization of due deadlines etc.
