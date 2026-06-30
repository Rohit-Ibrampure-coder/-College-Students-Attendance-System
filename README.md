# 🎓 College Attendance Management System

A modern **College Attendance Management System** built using **Flask**, **MySQL**, **Bootstrap 5**, and **SQLAlchemy**. The system provides secure role-based access for **Admin**, **Teacher**, and **Student**, allowing efficient student management, attendance tracking, reporting, and analytics.

---

## ✨ Features

### 🔐 Authentication

- Secure Login System
- Password Hashing
- Role-Based Access Control
- Admin, Teacher and Student Portals

---

## 👨‍🏫 Admin & Teacher Features

### 📚 Student Management

- Add Student
- Edit Student
- Delete Student
- Search Students
- Filter by Course
- Filter by Academic Year
- Automatic Student Login Account Creation

---

### ✅ Attendance Management

- Mark Daily Attendance
- Edit Attendance
- Delete Attendance
- Prevent Duplicate Attendance Records
- Filter Students by Course and Year

---

### 📊 Attendance Reports

- Search Attendance by Date
- Filter by Course
- Filter by Year
- Edit Attendance Records
- Delete Attendance Records
- Download Attendance Report as PDF

---

### 📈 Attendance Summary

- Student-wise Attendance Percentage
- Present Days
- Absent Days
- Low Attendance Identification
- View Student Attendance History
- Download Individual Student PDF Report

---

### 📉 Dashboard

- Total Students
- Attendance Records
- Present Today
- Absent Today
- Low Attendance Students
- Attendance Charts
- Student Distribution by Year

---

## 🎓 Student Portal

Students can securely log in using their registered email address.

### Student Dashboard

- Welcome Dashboard
- Total Classes
- Present Days
- Absent Days
- Attendance Percentage
- Attendance Status

### My Attendance

- View Personal Attendance Records
- Date-wise Attendance History

### Attendance Summary

- Present Days
- Absent Days
- Total Classes
- Attendance Percentage
- Attendance Progress

### My Profile

- Student Information
- Roll Number
- Course
- Year
- Email
- Phone Number

### Download Report

- Download Personal Attendance Report in PDF Format

---

## 🛠 Technology Stack

### Backend

- Python
- Flask
- SQLAlchemy

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Bootstrap Icons

### Database

- MySQL

### PDF Generation

- ReportLab

### Authentication

- Flask-Login
- Werkzeug Security

---


## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/Rohit-Ibrampure-coder/College-Students-Attendance-System.git
```

---

### Move into Project

```bash
cd College-Students-Attendance-System
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

---

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Database

Create a MySQL database.

Example:

```sql
CREATE DATABASE attendance_system;
```

Update your database credentials in `config.py`.

---

### Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 👥 Default User Roles

### Admin

- Full System Access

### Teacher

- Student Management
- Attendance Management
- Reports
- Attendance Summary

### Student

- Dashboard
- My Attendance
- Attendance Summary
- My Profile
- Download Attendance Report

---

## 🔒 Security Features

- Password Hashing
- Role-Based Authorization
- Login Required Protection
- Duplicate Attendance Prevention
- Duplicate Email Validation
- Duplicate Roll Number Validation
- Duplicate Phone Number Validation


---

## 👨‍💻 Developer

**Rohit Ibrampure**

BCA Student

Built as a portfolio project using Flask and MySQL.
