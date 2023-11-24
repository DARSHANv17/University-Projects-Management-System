show databases;
CREATE DATABASE project_db;
use project_db;


CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE domains (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  file longblob,
  studentID INT NOT NULL,
  domainID INT NOT NULL,
  status ENUM('approved', 'rejected','pending') DEFAULT 'pending' NOT NULL,
  FOREIGN KEY (studentID) REFERENCES users(id),
  FOREIGN KEY (domainID) REFERENCES domains(id)
);

CREATE TABLE faculties (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE comments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  text TEXT NOT NULL,
  projectID INT NOT NULL,
  studentID INT NOT NULL,
  FOREIGN KEY (projectID) REFERENCES projects(id),
  FOREIGN KEY (studentID) REFERENCES users(id)
);

INSERT INTO domains (name) VALUES ('DBMS');
INSERT INTO domains (name) VALUES ('AI/ML');
INSERT INTO domains (name) VALUES ('AR/VR');
INSERT INTO domains (name) VALUES ('CYBER SECURITY');
INSERT INTO domains (name) VALUES ('ROBOTICS');
INSERT INTO domains (name) VALUES ('IOT');
INSERT INTO domains (name) VALUES ('Other');



DELIMITER //

CREATE PROCEDURE ValidateEmail(email VARCHAR(255))
BEGIN
    IF POSITION('@' IN email) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER BeforeInsertTrigger
BEFORE INSERT ON users -- Assuming your table name is 'users'
FOR EACH ROW
BEGIN
    CALL ValidateEmail(NEW.email);
END;

//

DELIMITER ;







show tables;

select * from users;
select * from projects;
select * from comments;
select * from faculties;
select * from domains;








