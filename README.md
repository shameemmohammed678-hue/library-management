📚 Library Management System (Python + Streamlit + MySQL)

A complete Library Management System built using Python, Streamlit, and MySQL.
The application supports Admin and User login, book management, borrowing/return features, and a clean UI built with Streamlit.📚 Library Management System (Python + Streamlit + MySQL)

🚀 Features
🔐 Authentication

Login system with Admin and User roles

Role-based access control

📖 Book Management (Admin)

Add new books

Remove books

Update available quantity

Check if a book exists

🔍 Book Search (All Users)

Search books by:

Title

Author

Publisher

Genre

Book ID

📚 Borrow & Return System

Borrow books (updates DB automatically)

Return books

Tracks availability in real time

🛠️ Tech Stack
Component	Technology
Backend	Python
UI	Streamlit
Database	MySQL
ORM/Driver	PyMySQL

📂 Project Structure
Library-App/
│── app.py                # Main Streamlit application
│── librarydb.py          # Database connection and queries
│── requirements.txt      # Python dependencies
│── README.md             # Documentation
│── assets/               # (Optional) screenshots

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone <your-repo-link>
cd Library-App

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Create MySQL Database
CREATE DATABASE librarydb;
USE librarydb;

4️⃣ Create users and books tables

(Replace with your actual schema)

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(100),
    role VARCHAR(10)
);

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    publisher VARCHAR(100),
    genre VARCHAR(50),
    pub_year INT,
    available_quantity INT
);

5️⃣ Update DB credentials

In librarydb.py:

self.con = pymysql.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="librarydb",
    port=3306
)

6️⃣ Run the app
streamlit run app.py

🌐 IMPORTANT NOTE ABOUT ONLINE DEPLOYMENT

This project uses a local MySQL database.
When you run the app using a shared Streamlit link, the database cannot connect.
So login will show USER NOT FOUND.

👉 Run the app locally for full functionality.
👉 This is normal for backend projects.

