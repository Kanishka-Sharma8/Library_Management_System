CREATE DATABASE Library_Management_System;
USE Library_Management_System;

CREATE TABLE Books (
    SerialNo INT AUTO_INCREMENT PRIMARY KEY,
    BookName VARCHAR(50) NOT NULL,
    AuthorName VARCHAR(50) NOT NULL,
    TotalBooks INT NOT NULL CHECK (TotalBooks >= 0)
);

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50) NOT NULL,
    Role ENUM('admin', 'user') NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    SerialNo INT,
    IssueDate DATE NOT NULL,
    ReturnDate DATE NOT NULL,
    FinePaid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (SerialNo) REFERENCES Books(SerialNo)
);

INSERT INTO Books (BookName, AuthorName, TotalBooks) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 5),
('To Kill a Mockingbird', 'Harper Lee', 7),
('1984', 'George Orwell', 4),
('Pride and Prejudice', 'Jane Austen', 6),
('The Catcher in the Rye', 'J.D. Salinger', 3),
('The Hobbit', 'J.R.R. Tolkien', 5),
('Moby Dick', 'Herman Melville', 2),
('War and Peace', 'Leo Tolstoy', 4),
('The Odyssey', 'Homer', 3),
('Crime and Punishment', 'Fyodor Dostoevsky', 4);

INSERT INTO Users (UserName, Role, Password) VALUES
('admin1', 'admin', 'adminpass1'),
('user1', 'user', 'userpass1'),
('user2', 'user', 'userpass2');