# Attendance Tracker
A Python and MySQL based Attendance Tracker that allows users to manage students and maintain attendance records.

## Features

### Student Management
- Add new students
- View all students
- Search students by roll number or name
- Delete students
- Prevent duplicate roll numbers
- Prevent deletion when attendance records exist

### Attendance Management
- Mark student attendance
- Record Present or Absent status
- Prevent duplicate attendance for the same student, date, and subject
- View attendance records for a student
- View attendance records by date
- Calculate attendance percentage

## Technologies Used
- Python
- MySQL
- mysql-connector-python
- python-dotenv
- Git
- GitHub

## Project Structure

Attendance_Tracker/
│
├── attendance.py
├── student.py
├── database.py
├── main.py
├── database.sql
├── requirements.txt
├── README.md
├── .gitignore
└── .env