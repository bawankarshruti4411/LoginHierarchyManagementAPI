CREATE DATABASE IF NOT EXISTS hierarchy_db;

USE hierarchy_db;

-- ==========================================
-- SUPER ADMINS
-- ==========================================

CREATE TABLE super_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- COMPANY ADMINS
-- ==========================================

CREATE TABLE company_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- COMPANY USERS
-- ==========================================

CREATE TABLE company_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_company_user_admin
    FOREIGN KEY (admin_id)
    REFERENCES company_admins(id)
    ON DELETE CASCADE
);

-- ==========================================
-- MASTERS
-- ==========================================

CREATE TABLE masters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- OPERATIONS
-- ==========================================

CREATE TABLE operations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operation_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- USER OPERATIONS
-- ==========================================

CREATE TABLE user_operations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    operation_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_operations_user
    FOREIGN KEY (user_id)
    REFERENCES company_users(id)
    ON DELETE CASCADE,

    CONSTRAINT fk_user_operations_operation
    FOREIGN KEY (operation_id)
    REFERENCES operations(id)
    ON DELETE CASCADE
);

-- ==========================================
-- DEFAULT DATA
-- ==========================================

INSERT INTO super_admins (
    email,
    password
)
VALUES (
    'superadmin@gmail.com',
    'admin123'
);

INSERT INTO company_admins (
    id,
    name,
    email,
    password
)
VALUES (
    1,
    'John Admin',
    'admin@company.com',
    'admin123'
);

INSERT INTO company_users (
    id,
    name,
    email,
    password,
    admin_id
)
VALUES
(
    1,
    'Rahul Sharma',
    'rahul@gmail.com',
    '1234',
    1
),
(
    2,
    'Priya Singh',
    'priya@gmail.com',
    '1234',
    1
),
(
    3,
    'Amit Kumar',
    'amit@gmail.com',
    '1234',
    1
),
(
    4,
    'Neha Patel',
    'neha@gmail.com',
    '1234',
    1
);

INSERT INTO masters (
    id,
    name,
    description
)
VALUES
(
    1,
    'Customer Master',
    'Stores customer details'
),
(
    2,
    'Vendor Master',
    'Stores vendor details'
),
(
    3,
    'Employee Master',
    'Stores employee records'
),
(
    4,
    'Product Master',
    'Stores product information'
);

INSERT INTO operations (
    id,
    operation_name,
    description
)
VALUES
(
    1,
    'Create Customer',
    'Add new customer'
),
(
    2,
    'Update Customer',
    'Modify customer'
),
(
    3,
    'Delete Customer',
    'Remove customer'
),
(
    4,
    'Generate Report',
    'Generate reports'
),
(
    5,
    'Export Data',
    'Export system data'
),
(
    6,
    'Approve Order',
    'Approve customer orders'
),
(
    7,
    'Manage Inventory',
    'Inventory management'
);

INSERT INTO user_operations (
    user_id,
    operation_id
)
VALUES
(1,1),
(1,2),

(2,2),
(2,4),
(2,5),

(3,1),
(3,6),
(3,7),

(4,4),
(4,5);

-- ==========================================
-- INDEXES
-- ==========================================

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
