## Library Management System with Tkinter - Python

This is a Python code for a Library Management System using Tkinter for the graphical user interface. It allows users to register, login, and manage library resources like books and rental requests depending on their role (Guest or Librarian).

**Here's a breakdown of the code and the functionalities it offers:**

**1. Imports:**

- `tkinter`: This library is used for creating the graphical user interface (GUI) elements.
- `sqlite3`: This library is used to interact with the SQLite database to store library data.
- `simpledialog` and `messagebox`: These are submodules of `tkinter` used for creating pop-up windows for user interaction like input and displaying messages.

**2. Database Connection:**

- The code establishes a connection to the SQLite database named `library.db`.
- A cursor object is created to execute SQL queries and interact with the database.

**3. `LibraryApp` Class:**

- This class represents the main application window.
- It defines methods for:
    - Creating the login screen with username, password, and role selection.
    - Validating user login credentials against the database.
    - Creating separate dashboards for Guest and Librarian roles.
    - Handling user functionalities based on their role:
        - Guests can view books, request books, return books, view their rented books, and see registered users.
        - Librarians can perform all guest functionalities along with adding new books, removing books, approving book rental requests, and viewing registered users.
- It leverages pop-up windows using `simpledialog` and `messagebox` for user interaction like entering data and displaying messages.

**4. Database Table Creation (if not exists):**

- The code uses SQL commands to create three tables in the database:
    - `users`: Stores user information (username, password, role).
    - `books`: Stores book information (title, author, rented status).
    - `rental_requests`: Stores rental request information (user, book, approval status).

**5. Main Execution:**

- The code checks if the script is run directly (`__name__ == "__main__"`). 
- If true, it creates an instance of the `LibraryApp` class and starts the main event loop (`mainloop`) to run the application.

"# Library-Management-System" 
"# Library-Management-System" 
"# Library-Management-System" 
"# Library-Manager" 
