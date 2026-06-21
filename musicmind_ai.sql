CREATE DATABASE IF NOT EXISTS musicmind_ai;

USE musicmind_ai;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student','admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RESULTS TABLE
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    personality VARCHAR(100),
    genre VARCHAR(100),
    score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OTP TABLE
CREATE TABLE IF NOT EXISTS password_resets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    otp VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DEFAULT ADMIN
INSERT INTO users(username,email,password,role)
VALUES(
'admin',
'admin@musicmind.com',
'$2b$12$9t4q7Y4X1uN1p4v7kJjK1eJQx7I1B1s0P8v8eM3vP2vXxWmN9lN6W',
'admin'
);