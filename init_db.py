import mysql.connector
from config import DB_CONFIG


# Connect without database first
connection = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    port=DB_CONFIG["port"]
)

cursor = connection.cursor()

cursor.execute(
    "CREATE DATABASE IF NOT EXISTS customer_complaint_ai"
)

cursor.execute(
    "USE customer_complaint_ai"
)


# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role ENUM(
        'customer',
        'employee',
        'admin'
    ) DEFAULT 'customer',

    department VARCHAR(100),

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
)
""")


# COMPLAINT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (

    id INT AUTO_INCREMENT PRIMARY KEY,

    complaint_id VARCHAR(30)
    UNIQUE NOT NULL,

    user_id INT NOT NULL,

    subject VARCHAR(200) NOT NULL,

    description TEXT NOT NULL,

    category VARCHAR(100),

    confidence DECIMAL(5,2),

    sentiment VARCHAR(50),

    priority VARCHAR(50),

    department VARCHAR(100),

    status ENUM(
        'Pending',
        'Assigned',
        'In Progress',
        'Resolved',
        'Rejected'
    ) DEFAULT 'Pending',

    assigned_employee INT NULL,

    admin_response TEXT,

    employee_response TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

    FOREIGN KEY (assigned_employee)
    REFERENCES users(id)
    ON DELETE SET NULL
)
""")


# FEEDBACK
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (

    id INT AUTO_INCREMENT PRIMARY KEY,

    complaint_id INT NOT NULL,

    user_id INT NOT NULL,

    rating INT,

    comments TEXT,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (complaint_id)
    REFERENCES complaints(id)
    ON DELETE CASCADE,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
)
""")


connection.commit()

cursor.close()
connection.close()

print("Database created successfully!")
print("Tables created: users, complaints, feedback")