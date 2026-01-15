# CS50X PROJECT
My final project for the CS50X Python course.
# Travel Management System 🚍
Demo video link : https://youtu.be/T7iyCDJ_OCc          
##📌 Project Description

The Travel Management System is a web-based application developed for small school transportation businesses to manage students, fees, attendance, and vehicles in a simple and organized way. Many transport operators still rely on manual registers, notebooks, or messaging applications to maintain student records and payment details. This traditional approach often leads to disorganized data, missing records, and difficulty tracking fee payments and attendance history.

This project aims to solve these problems by providing a digital and centralized management system. The application allows an administrator to handle all transportation-related data from a single dashboard. With a secure login system, only authorized users can access and manage sensitive information such as student details and payment status.

After logging in, the admin can add and view students, track whether monthly fees are paid or unpaid, manage attendance records, and maintain vehicle information. All data is stored in a SQLite database, ensuring data persistence and easy retrieval. The system is designed to be lightweight, efficient, and suitable for daily real-world use.

The user interface is built using Bootstrap 5, making the application responsive and mobile-friendly. This allows transport operators to use the system on smartphones or tablets while working in the field. Overall, the Travel Management System provides a practical solution that reduces manual work, minimizes errors, and improves record management for school transport services.

🎯 Problem Statement

School transport operators often face difficulties such as:

Maintaining student records manually

Tracking monthly fee payments accurately

Managing attendance history

Handling vehicle-related information efficiently

This project addresses these issues by offering a simple, digital, and structured solution that improves efficiency and reliability.

✅ Features

🔐 Secure Admin Login

👦 Student Management (Add and View Students)

💰 Fee Management (Paid / Unpaid Tracking)

📋 Attendance Management (Expandable Feature)

🚌 Vehicle Management

📱 Mobile-Friendly Interface using Bootstrap 5

🗂️ Project Structure

app.py
The main Flask application file containing routes, application logic, and database interactions.

templates/
Contains all HTML files used to render different pages such as login, dashboard, student management, and fee pages.

static/
Stores CSS and frontend-related assets used for styling the application.

SQLite Database
Used to store student information, fee status, attendance data, and vehicle records.

🛠 Technologies Used

Python

Flask

SQLite

HTML & CSS

Bootstrap 5

🧠 Design Choices

Flask was chosen because it is lightweight, easy to use, and suitable for small to medium-sized web applications.

SQLite was used as the database because it is simple to set up and ideal for applications that do not require a separate database server.

Bootstrap 5 was selected to ensure a responsive and mobile-friendly user interface.

This project was chosen because it is based on a real-world problem and provides a practical solution that can be used daily.

▶️ How to Run the Project
pip install flask
flask run --host=0.0.0.0 --port=5000

🚀 Future Improvements

Monthly fee reports

Attendance history and analytics

Multiple admin accounts

Export data to PDF or Excel

SMS or Email notification system