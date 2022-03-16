# Report Triager

 ![paperplane](/static/images/lietadielko_rm.png)

[live demo](https://report-triager.herokuapp.com/) to your avail on Heroku 
# Description

## Background

This project was created for the CS50x course by HarvardX. Inspiration for this web application came from my job where I work as a pharmacovigilance specialist.

Pharmacovigilance is a slightly obscure field of pharmaceutical businesses related to drug safety. The main goal of pharmacovigilance is to steadily monitor and evaluate risks and benefits associated with use of medicinal drugs in humans. One of the most significant parts of this work is collection of adverse reactions reports related to use of medicinal products. Reports may be received from various sources, for example from health-care professionals, employees within pharmaceutical companies, but also directly from patients using the drug. Those reports need to be evaluated, tracked and administratively processed in order to allow monitoring of drug safety.

This tool - Report Triager - aims to help workers in pharmacovigilance to track incoming reports and organize their processing within project teams. Data necessary for report evaluation are inserted into Report Triager and can be updated/deleted in case of further changes in report evaluation later. In addition to storing information about reports, there is a possibility to create and assign relevant to do's with specific deadlines to various team members.

## Features

- registration and log-in of users
- overview of all tracked reports
- addition of new adverse drug reaction reports
- ability to edit/delete report details
- ability to create To do's associated to a particular report - To Do's are assigned to a specified user (team member)
- ability to mark complete, edit or delete individual To Do's
- overview of pending and completed To Do items (personal or all)
- ability to change user password/delete user account

# Set-up
If anyone would be interested to you use the code, I can only recommend installing dependencies as listed in requirements.txt. For creating db for the first time, uncomment line 73 in main.py (or add somewhere to the code 'db.create_all()').

# Technical solutions

## Backend
This application was build with Flask webframework 2.0.2 in Python 3.10. I have decided to use Flask due to its "lightweight" reputation and small size of the project in scope. For additional functionally Flask WTF, Flask Login and Flask SQLAlchemy were imported.

Flask WTF 1.0.0 allows integration of Flask with WTForms that were used for creation and validation of all forms in this web application. Forms classes were separated to the forms.py file.

In order to ensure basic login functionality and user session management Flask-Login 0.5.0 was used. For password encryption, PBKDF2 algorithm with SHA256 (from werkzeug.security) and some salting was used for registration/login of users.

A relational database SQLite was selected as a SQL database engine for the "draft" version of the project due to its easy manipulation, lightweight and sufficiency of features. However, as SQLite is file based and does not allow simultaneous concurrent writes (according the Internet), change to more complex database engine such as MySQL (or PostgreSQL) would be required in case of deployment of the application to a cloud based server.
(update:) For Heroku demo, database engine was switched to PostgreSQL.

SQL Alchemy 1.4.29 was implemented in order to facilitate manipulation between Python (Flask) and the relational database. The main advantage was its Object Relational Mapper (ORM) tool which allowed mapping of the database tables into python classes. SQL Alchemy was used in hope it would make upgrade from SQLite engine to more complex database engines significantly easier, if required in the future.

## Frontend 
Frontend of the application was built, unsurprisingly, with HTML and CSS with marginal implementation of own short scripts written in JavaScript. Bootstrap 5.1.3 was used as front-end framework mainly due to its ability to create minimalistic and responsive designs. Although this application was not intended for use on mobile devices, basic responsiveness was implemented by means of Bootstrap. Additional css media queries were added to improve responsiveness. Currently, mobile view requires some updates, especially in dashboard section.

The application consists of title page containing login and registration forms and internal, login protected "workspace". The workspace involves welcome overview page (incorrectly dubbed as dashboard) from which you can open a report and edit its details or add tasks to the report. Via side navbar you can redirect to task list or go to add new report page. Through the bottom part of the navbar you can logout or access account settings where you can delete your account or change password.

For webdesign, I have chosen minimalistic design focused on functionality. Two separate stylesheets were created - styles.css for title page and dashboard_style.css for internal "workspace". Side navbar was inspired from Bootstrap examples [side navbar](https://getbootstrap.com/docs/5.1/examples/sidebars/). Icons and illustration were drawn/edited by me, however, I took an inspiration and background materials from the internet: [dashboard icon](https://www.flaticon.com/free-icons/dashboard "created by Eucalyp - Flaticon"), and dashboard clock illustration [dashboard illustration](https://www.rikvin.com/blog/5-time-management-tips/ "author unknown"). 

# Future possibilities

- security - user account confirmation by administrator; confirmation of account via email
- security - for actual deployment of the application upgrade to other db system would be required
- user allocation to specific projects (separate log-ins)
- addition of visual metrics - graphs to see workload distribution within team; visualization of due deadlines etc.
# Thanks

Big thanks to the amazing course of 'CS50x' by HarvardX and '100 Days of Code: The Complete Python Pro Bootcamp for 2022' by Dr. Angela Yu.