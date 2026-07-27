import mysql.connector
from werkzeug.security import generate_password_hash
from config import DB_CONFIG


name = "System Admin"
email = "admin@smartcomplaint.com"
password = "Admin@123"

hashed_password = generate_password_hash(password)


connection = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    database=DB_CONFIG["database"],
    port=DB_CONFIG["port"]
)

cursor = connection.cursor()


cursor.execute(
    "SELECT id FROM users WHERE email = %s",
    (email,)
)

existing_admin = cursor.fetchone()


if existing_admin:

    print("Admin account already exists.")

else:

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password,
            role,
            department
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            name,
            email,
            hashed_password,
            "admin",
            "Administration"
        )
    )

    connection.commit()

    print("Admin account created successfully!")


cursor.close()
connection.close()