CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- TABLE MANAGERS
CREATE TABLE managers (
    manager_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE MEMBERS 
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    birthday DATETIME NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phoneNumber VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
);

-- TABLE BOOKS
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    pages INTEGER CHECK(pages > 0),
    publish_year INTEGER CHECK(publish_year > 0),
    status TINYINT DEFAULT 0 CHECK(status IN (0, 1, 2)), 
    book_type ENUM('novel', 'textbook', 'science') NOT NULL,
    genre VARCHAR(50),
    subject VARCHAR(50),
    level ENUM('primary', 'secondary', 'highschool'),
    field VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- TABLE BORROWS
CREATE TABLE borrows (
    borrow_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATE,
    due_date DATE NOT NULL,
    return_date DATE DEFAULT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);