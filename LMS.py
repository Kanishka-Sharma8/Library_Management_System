import mysql.connector
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def validate_login(role, user_id, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM Users WHERE UserName = %s AND Password = %s AND Role = %s"
    cursor.execute(query, (user_id, password, role))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        messagebox.showinfo("Success", f"Welcome {role}!")
        root.destroy() 
    else:
        messagebox.showerror("Error", "Invalid Credentials")


def show_login(role):
    global root
    root = tk.Tk()
    root.title("Library Management System")
    root.geometry("400x300")

    tk.Label(root, text="Library Management System", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(root, text="User ID:").pack()
    user_id_entry = tk.Entry(root)
    user_id_entry.pack()

    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login_action():
        user_id = user_id_entry.get()
        password = password_entry.get()
        validate_login(role, user_id, password)

    tk.Button(root, text="Login", command=login_action, width=10, bg="lightblue").pack(pady=10)
    tk.Button(root, text="Cancel", command=root.quit, width=10, bg="lightblue").pack()

    root.mainloop()


def ask_user_type():
    def set_role(user_role):
        user_choice.destroy()
        show_login(user_role)

    user_choice = tk.Tk()
    user_choice.title("Select Role")
    user_choice.geometry("300x200")

    tk.Label(user_choice, text="Are you an Admin or a User?", font=("Arial", 12)).pack(pady=10)
    tk.Button(user_choice, text="Admin", command=lambda: set_role("admin"), width=10, bg="lightblue").pack(pady=5)
    tk.Button(user_choice, text="User", command=lambda: set_role("user"), width=10, bg="lightblue").pack(pady=5)

    user_choice.mainloop()

ask_user_type()

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root890",  
        database="Library_Management_System"
    )

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            SerialNo INT AUTO_INCREMENT PRIMARY KEY,
            BookName VARCHAR(50) NOT NULL,
            AuthorName VARCHAR(50) NOT NULL,
            TotalBooks INT NOT NULL CHECK (TotalBooks >= 0)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserID INT AUTO_INCREMENT PRIMARY KEY,
            UserName VARCHAR(50) NOT NULL,
            Role ENUM('admin', 'user') NOT NULL,
            Password VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INT AUTO_INCREMENT PRIMARY KEY,
            UserID INT,
            SerialNo INT,
            IssueDate DATE NOT NULL,
            ReturnDate DATE NOT NULL,
            FinePaid BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (SerialNo) REFERENCES Books(SerialNo)
        )
    """)
    conn.commit()
    conn.close()

def add_book(book_name, author_name, total_books):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (BookName, AuthorName, TotalBooks) VALUES (%s, %s, %s)",
                   (book_name, author_name, total_books))
    conn.commit()
    conn.close()
    print("Book added successfully!")

def issue_book(user_id, serial_no):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT TotalBooks FROM Books WHERE SerialNo = %s", (serial_no,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        issue_date = datetime.today().date()
        return_date = issue_date + timedelta(days=15)
        cursor.execute("INSERT INTO Transactions (UserID, SerialNo, IssueDate, ReturnDate) VALUES (%s, %s, %s, %s)",
                       (user_id, serial_no, issue_date, return_date))
        cursor.execute("UPDATE Books SET TotalBooks = TotalBooks - 1 WHERE SerialNo = %s", (serial_no,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book not available!")
    conn.close()

def return_book(transaction_id, return_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SerialNo, ReturnDate FROM Transactions WHERE TransactionID = %s", (transaction_id,))
    result = cursor.fetchone()
    if result:
        serial_no, expected_return_date = result
        cursor.execute("UPDATE Books SET TotalBooks = TotalBooks + 1 WHERE SerialNo = %s", (serial_no,))
        if return_date > expected_return_date:
            print("Fine must be paid before completing return.")
        else:
            print("Book returned successfully!")
        conn.commit()
    else:
        print("Invalid transaction ID!")
    conn.close()

def add_user(username, role, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (UserName, Role, Password) VALUES (%s, %s, %s)",
                   (username, role, password))
    conn.commit()
    conn.close()
    print("User added successfully!")



def main():
    create_tables()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Add User")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            name = input("Enter book name: ")
            author = input("Enter author name: ")
            total = int(input("Enter total copies: "))
            add_book(name, author, total)
        elif choice == '2':
            user_id = int(input("Enter User ID: "))
            serial = int(input("Enter Serial No of book to issue: "))
            issue_book(user_id, serial)
        elif choice == '3':
            transaction_id = int(input("Enter Transaction ID: "))
            return_date = input("Enter return date (YYYY-MM-DD): ")
            return_book(transaction_id, datetime.strptime(return_date, "%Y-%m-%d").date())
        elif choice == '4':
            username = input("Enter username: ")
            role = input("Enter role (admin/user): ")
            password = input("Enter password: ")
            add_user(username, role, password)
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

 