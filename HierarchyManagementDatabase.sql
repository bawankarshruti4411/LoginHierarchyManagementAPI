create database hierarchy_db;
USE hierarchy_db;

CREATE TABLE company_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE company_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    admin_id INT,

    FOREIGN KEY (admin_id)
    REFERENCES company_admins(id)
);

CREATE TABLE masters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

CREATE TABLE operations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operation_name VARCHAR(100),
    description TEXT
);

CREATE TABLE user_operations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,
    operation_id INT,

    FOREIGN KEY(user_id)
    REFERENCES company_users(id),

    FOREIGN KEY(operation_id)
    REFERENCES operations(id)
);

INSERT INTO company_admins
(id, name, email, password)
VALUES
(1,'John Admin','admin@company.com','admin123');

INSERT INTO company_users (id, name, email, password, admin_id) VALUES
(1,'Rahul Sharma','rahul@gmail.com','1234',1),
(2,'Priya Singh','priya@gmail.com','1234',1),
(3,'Amit Kumar','amit@gmail.com','1234',1),
(4,'Neha Patel','neha@gmail.com','1234',1);

INSERT INTO masters (id,name,description) VALUES
(1,'Customer Master','Stores customer details'),
(2,'Vendor Master','Stores vendor details'),
(3,'Employee Master','Stores employee records'),
(4,'Product Master','Stores product information');

INSERT INTO operations (id,operation_name,description) VALUES
(1,'Create Customer','Add new customer'),
(2,'Update Customer','Modify customer'),
(3,'Delete Customer','Remove customer'),
(4,'Generate Report','Generate reports'),
(5,'Export Data','Export system data'),
(6,'Approve Order','Approve customer orders'),
(7,'Manage Inventory','Inventory management');

INSERT INTO user_operations (id,user_id,operation_id) VALUES
-- Rahul
(1,1,1),
(2,1,2),
-- Priya
(3,2,2),
(4,2,4),
(5,2,5),
-- Amit
(6,3,1),
(7,3,6),
(8,3,7),
-- Neha
(9,4,4),
(10,4,5);

CREATE INDEX idx_admin_email
ON company_admins(email);

CREATE INDEX idx_user_email
ON company_users(email);

CREATE INDEX idx_user_operations_user
ON user_operations(user_id);

CREATE INDEX idx_user_operations_operation
ON user_operations(operation_id);

CREATE INDEX idx_user_operations_composite
ON user_operations(user_id, operation_id);
