import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time
import sys

class UserInterface:
    def __init__(self, app_name):
        self.app_name = app_name
        self.connection = None
        self.user_id = None
        self.email_address = None

    def connect_to_database(self):
        mycon = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='to_do_list')
        return mycon

    def create_user_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(50) NOT NULL,
                email VARCHAR(255) UNIQUE,
                phone_number VARCHAR(11) UNIQUE, 
                username VARCHAR(50), 
                password VARCHAR(50)
            )
        """)

        # cursor.execute("ALTER TABLE users ADD COLUMN password VARCHAR(50);")

        self.connection.commit()

    def create_todo_list_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo_list (
                user_id INT,
                task VARCHAR(255) NOT NULL,
                deadline DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.connection.commit()

    def display_menu(self):
        print(f"\nWelcome to {self.app_name} application")
        print("""
            1. Sign up
            2. Log in
            3. Reset Password/Username
            4. Quit
        """)

    def signup(self):
        query = "INSERT INTO users (fullname, email, phone_number, username, password) VALUES(%s,%s,%s,%s,%s)"
        time.sleep(1)
        print('''
            Sign up page
        ''')
        fullname = input("\nFullname: ")
        email_address = input("\nEmail address: ")
        phone_number = input("\nPhone number: ")
        username = input("\nUsername: ")
        password = input("\nPassword: ")

        cursor = self.connection.cursor()
        val = (fullname, email_address, phone_number, username, password)
        cursor.execute(query, val)
        self.connection.commit()
        print('\nPlease wait...')
        time.sleep(2)
        print("\nLoading...")
        time.sleep(3)
        print("\nSuccessfully registered")

    def log_in(self):
        query = "SELECT id FROM users WHERE username = %s AND password = %s"
        time.sleep(1)
        print('''
            Log in page
        ''')
        username = input("\nUsername: ")
        password = input("\nPassword: ")

        cursor = self.connection.cursor()
        val = (username, password)
        cursor.execute(query, val)
        result = cursor.fetchone()

        if result:
            self.user_id = result[0]
            print('\nPlease wait...')
            time.sleep(1.5)
            print("\nLoading...")
            time.sleep(2)
            self.home_page()
        else:
            print(f"\nWrong password or username!")

    def reset_credentials(self):
        email = input("\nEnter your Email: ")
        query = "SELECT username, password FROM users WHERE email = %s"
        
        cursor = self.connection.cursor()
        val = (email,)
        cursor.execute(query, val)
        result = cursor.fetchone()

        if result:
            username, password = result
            print(f"\nYour current details:")
            print(f"Username: {username}")
            print(f"Password: {password}")

            choice = input("\nPress 'a' to reset password, 'b' to reset username, or any other key to cancel: ")

            if choice.lower() == 'a':
                new_password = input("\nEnter your new password: ")
                confirm_password = input("Confirm your new password: ")

                if new_password == confirm_password:
                    update_query = "UPDATE users SET password = %s WHERE email = %s"
                    update_val = (new_password, email)
                    cursor.execute(update_query, update_val)
                    self.connection.commit()
                    print("\nPassword reset successfully.")
                else:
                    print("\nPasswords do not match. Password reset failed.")
            elif choice.lower() == 'b':
                new_username = input("\nEnter your new username: ")
                confirm_username = input("Confirm your new username: ")

                if new_username == confirm_username:
                    update_query = "UPDATE users SET username = %s WHERE email = %s"
                    update_val = (new_username, email)
                    cursor.execute(update_query, update_val)
                    self.connection.commit()
                    print("\nUsername reset successfully.")
                else:
                    print("\nUsernames do not match. Username reset failed.")
            else:
                print("\nReset cancelled.")
        else:
            print('\nNo user found with the provided email address.')

    def home_page(self):
        time.sleep(2)
        print("Home page".center(180))
        print(f"""
            Welcome back {self.app_name}
        """)

        while True:
            print("""
                1. Add task with deadline
                2. Display to-do list
                3. Quit
            """)

            user_choice = input("\nEnter your choice: ")

            if user_choice == "1":
                self.add_task_with_deadline()
            elif user_choice == "2":
                self.display_todo_list()
            elif user_choice == "3":
                self.quit()
            else:
                print("\nInvalid input! Please enter a number between 1 and 3.")

    def initialize(self):
        self.connection = self.connect_to_database()
        self.create_user_table()
        self.create_todo_list_table()

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-4): ")

            if choice == "1":
                self.initialize()
                self.signup()
            elif choice == "2":
                self.initialize()
                self.log_in()
            elif choice == "3":
                self.initialize()
                self.reset_credentials()
            elif choice == "4":
                print("\nQuitting the to-do list application. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.")

    def add_task_with_deadline(self):
        task = input("\nEnter the task: ")
        deadline_str = input("\nEnter the deadline (format: YYYY-MM-DD HH:MM): ")

        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            self.add_task_to_database(task, deadline)
        except ValueError:
            print("\nInvalid deadline format. Please use YYYY-MM-DD HH:MM.")

    def add_task_to_database(self, task, deadline):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO todo_list (user_id, task, deadline) VALUES (%s, %s, %s)
        """, (self.user_id, task, deadline))
        self.connection.commit()
        print(f"\nTask '{task}' added to your to-do list with a deadline of {deadline}.")

    def display_todo_list(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT task, deadline FROM todo_list WHERE user_id = %s
        """, (self.user_id,))

        result = cursor.fetchall()

        if not result:
            print("\nYour to-do list is empty.")
        else:
            print("\nYour to-do list:")
            for task, deadline in result:
                print(f"{task}: Deadline - {deadline}")

    def quit(self):
        print("\nQuitting the to-do list application. Goodbye!")
        sys.exit()

if __name__ == "__main__":
    app = UserInterface("My To-Do List")
    app.run()
