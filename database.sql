CREATE DATABASE IF NOT EXISTS attendance_db;

USE attendance_db;


CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    subject VARCHAR(100) NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,

    CONSTRAINT fk_attendance_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT unique_attendance
        UNIQUE (student_id, attendance_date, subject)
);


SHOW TABLES;