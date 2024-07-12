-- Create the database
CREATE DATABASE IF NOT EXISTS quad;
USE quad;

-- Table to store student information
CREATE TABLE IF NOT EXISTS student5 (
    StudentID VARCHAR(11) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE
);

-- Table to store candidate information
CREATE TABLE IF NOT EXISTS candidate5 (
    StudentID VARCHAR(11) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Department VARCHAR(100) NOT NULL,
    Semester VARCHAR(10) NOT NULL,
    BallotName VARCHAR(100) NOT NULL,
    Position VARCHAR(100) NOT NULL,
    INDEX idx_candidate_name (Name) -- Index on the 'Name' column
);

-- Table to store voting information
CREATE TABLE IF NOT EXISTS vote5 (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID VARCHAR(11) NOT NULL,
    CandidateName VARCHAR(100) NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES student5(StudentID),
    FOREIGN KEY (CandidateName) REFERENCES candidate5(Name)
);
