CREATE DATABASE IF NOT EXISTS course_registration;
USE course_registration;

-- TABLE TEACHERS
CREATE TABLE teachers (
    teacherId VARCHAR(255) PRIMARY KEY,
    fullName VARCHAR(255) NOT NULL,
    birthday DATETIME NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phoneNumber VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    userName VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- TABLE STUDENTS
CREATE TABLE students (
    studentId VARCHAR(255) PRIMARY KEY,
    fullName VARCHAR(255) NOT NULL,
    birthday DATETIME NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phoneNumber VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- TABLE COURSES
CREATE TABLE courses (
    courseId VARCHAR(255) PRIMARY KEY,
    courseName VARCHAR(255) NOT NULL,
    description TEXT,
    credits INT NOT NULL CHECK(credits > 0),
    teacherId VARCHAR(255),
    FOREIGN KEY (teacherId) REFERENCES teachers(teacherId)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- TABLE ENROLLMENTS
CREATE TABLE enrollments (
    enrollmentId VARCHAR(255) PRIMARY KEY,
    studentId VARCHAR(255) NOT NULL,
    courseId VARCHAR(255) NOT NULL,
    enrollmentDay DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    grade FLOAT CHECK(grade >= 0.0 AND grade <= 10.0),
    FOREIGN KEY (studentId) REFERENCES students(studentId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (courseId) REFERENCES courses(courseId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
