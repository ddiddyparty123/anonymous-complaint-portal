CREATE DATABASE IF NOT EXISTS student_complaints
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_complaints;

CREATE TABLE IF NOT EXISTS teacher_complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    complaint TEXT NOT NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE IF NOT EXISTS principal_complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    complaint TEXT NOT NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

CREATE TABLE IF NOT EXISTS environment_complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    complaint TEXT NOT NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending'
);

-- Optional: view complaints in MySQL Workbench
-- SELECT * FROM teacher_complaints ORDER BY submitted_at DESC;
-- SELECT * FROM principal_complaints ORDER BY submitted_at DESC;
-- SELECT * FROM environment_complaints ORDER BY submitted_at DESC;
