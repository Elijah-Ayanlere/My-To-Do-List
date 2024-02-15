# My To-Do List Application

Welcome to the My To-Do List application! This is a simple to-do list manager that allows users to sign up, log in, add tasks with deadlines, display their to-do list, and reset passwords or usernames.

## Features

- **Sign Up:** Create a new account with your name, email, phone number, username, and password.
- **Log In:** Log in to your account to access your personalized to-do list.
- **Add Task with Deadline:** Add tasks to your to-do list with specified deadlines.
- **Display To-Do List:** View your current to-do list with tasks and deadlines.
- **Reset Password/Username:** Reset your password or username if needed.

## Prerequisites

- Python 3.x
- MySQL Database

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Elijah-Ayanlere/your-to-do-list-repo.git

1. Install required Python packages:

   ```bash
     pip install mysql-connector-python
   
3. Create a MySQL database named to_do_list and ensure you have a MySQL server running.
4. Execute the SQL script database_setup.sql to set up the initial database structure.
5. Run the application:

   ```bash
    python3 to-do-list.py

## Database Schema

The application uses a MySQL database with the following schema:

**users:** Stores user information.

- id (Primary Key)
- fullname
- email (Unique)
- phone_number (Unique)
- username
- password

**todo_list:** Stores user tasks with deadlines.

user_id (Foreign Key referencing users.id)
task
deadline

## Contributing
Feel free to contribute to the development of this to-do list application by submitting issues or pull requests.

## License
This project is licensed under the MIT License.
