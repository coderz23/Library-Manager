import tkinter as tk
from tkinter import simpledialog, messagebox
from database import cursor, conn
from utils import clean_up_requests

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")  # Set the window title
        self.geometry("600x400")  # Set the window size
        self.create_login_widgets()  # Initialize login widgets

    def create_login_widgets(self):
        # Create and display login widgets
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        tk.Label(self.login_frame, text="Role").grid(row=2, column=0)

        self.username_entry = tk.Entry(self.login_frame)  # Entry for username
        self.password_entry = tk.Entry(self.login_frame, show='*')  # Entry for password

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        self.role_var = tk.StringVar()
        self.role_var.set("Guest")  # Default role is Guest

        tk.OptionMenu(self.login_frame, self.role_var, "Guest", "Librarian").grid(row=2, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=3, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=4, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Validate user credentials and role
        cursor.execute('SELECT role FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user and user[0] == role:
            self.role = user[0]
            self.create_dashboard()  # Create dashboard based on role
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = simpledialog.askstring("Register", "Enter username:")
        password = simpledialog.askstring("Register", "Enter password:")
        role = self.role_var.get()

        if username and password and role in ["Guest", "Librarian"]:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
        else:
            messagebox.showerror("Error", "Invalid input or role")

    def create_dashboard(self):
        self.login_frame.pack_forget()  # Hide login frame

        if self.role == "Guest":
            self.guest_frame = tk.Frame(self)
            self.guest_frame.pack(pady=20)
            # Guest-specific buttons
            tk.Button(self.guest_frame, text="View Books", command=self.view_books).pack(pady=5)
            tk.Button(self.guest_frame, text="Request Book", command=self.request_book).pack(pady=5)
            tk.Button(self.guest_frame, text="Return Book", command=self.return_book).pack(pady=5)
            tk.Button(self.guest_frame, text="View My Books", command=lambda: self.view_my_books(self.username_entry.get())).pack(pady=5)
            tk.Button(self.guest_frame, text="View Registered Guests", command=self.view_guests).pack(pady=5)
            tk.Button(self.guest_frame, text="View Registered Librarians", command=self.view_librarians).pack(pady=5)
            tk.Button(self.guest_frame, text="Logout", command=self.logout).pack(pady=10)
        
        elif self.role == "Librarian":
            self.librarian_frame = tk.Frame(self)
            self.librarian_frame.pack(pady=20)
            # Librarian-specific buttons
            tk.Button(self.librarian_frame, text="View Books", command=self.view_books).pack(pady=5)
            tk.Button(self.librarian_frame, text="Add Book", command=self.add_book).pack(pady=5)
            tk.Button(self.librarian_frame, text="Remove Book", command=self.remove_book).pack(pady=5)
            tk.Button(self.librarian_frame, text="Approve Requests", command=self.approve_requests).pack(pady=5)
            tk.Button(self.librarian_frame, text="View Registered Guests", command=self.view_guests).pack(pady=5)
            tk.Button(self.librarian_frame, text="View Registered Librarians", command=self.view_librarians).pack(pady=5)
            tk.Button(self.librarian_frame, text="Logout", command=self.logout).pack(pady=10)

    def request_book(self):
        book_id = simpledialog.askinteger("Request Book", "Enter Book ID")
        username = self.username_entry.get()

        if book_id:
            cursor.execute('SELECT is_rented FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()

            if book and book[0] == 0:
                cursor.execute('SELECT COUNT(*) FROM rental_requests WHERE username = ? AND book_id = ?', (username, book_id))
                request_count = cursor.fetchone()[0]

                if request_count == 0:
                    cursor.execute('INSERT INTO rental_requests (username, book_id, is_approved) VALUES (?, ?, 0)', (username, book_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Request sent to librarian")
                else:
                    messagebox.showerror("Error", "You have already requested this book")
            else:
                messagebox.showerror("Error", "Book is already rented")
        else:
            messagebox.showerror("Error", "Invalid Book ID")

    def return_book(self):
        book_id = simpledialog.askinteger("Return Book", "Enter Book ID")
        username = self.username_entry.get()

        if book_id:
            cursor.execute('SELECT id FROM rental_requests WHERE username = ? AND book_id = ? AND is_approved = 1', (username, book_id))
            request = cursor.fetchone()

            if request:
                cursor.execute('UPDATE books SET is_rented = 0 WHERE id = ?', (book_id,))
                cursor.execute('DELETE FROM rental_requests WHERE username = ? AND book_id = ? AND is_approved = 1', (username, book_id))
                conn.commit()
                messagebox.showinfo("Success", "Book returned")
            else:
                messagebox.showerror("Error", "No such rental request found")
        else:
            messagebox.showerror("Error", "Invalid Book ID")

    def add_book(self):
        title = simpledialog.askstring("Add Book", "Enter Book Title")
        author = simpledialog.askstring("Add Book", "Enter Book Author")

        if title and author:
            cursor.execute('INSERT INTO books (title, author, is_rented) VALUES (?, ?, 0)', (title, author))
            conn.commit()
            messagebox.showinfo("Success", "Book added")
        else:
            messagebox.showerror("Error", "Invalid input")

    def remove_book(self):
        book_id = simpledialog.askinteger("Remove Book", "Enter Book ID")

        if book_id:
            cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            book = cursor.fetchone()

            if book:
                cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book removed")
            else:
                messagebox.showerror("Error", "Book ID not found")
        else:
            messagebox.showerror("Error", "Invalid Book ID")

    def approve_requests(self):
        # Fetch and display rental requests to approve
        cursor.execute('''
            SELECT r.id, r.username, r.book_id, b.title
            FROM rental_requests r
            JOIN books b ON r.book_id = b.id
            WHERE r.is_approved = 0
            AND b.is_rented = 0
        ''')
        requests = cursor.fetchall()

        request_list = "\n".join([f"ID: {request[0]}, Book: {request[3]}, User: {request[1]}" for request in requests])

        requests_window = tk.Toplevel(self)
        requests_window.title("Approve Requests")
        requests_window.geometry("400x400")

        tk.Label(requests_window, text="Approve Requests", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(requests_window, wrap="word", height=15, width=50, padx=10, pady=10)
        text_widget.insert(tk.END, request_list)
        text_widget.pack()

        def approve_request():
            request_id = simpledialog.askinteger("Approve Request", "Enter Request ID to Approve")
            if request_id:
                cursor.execute('SELECT book_id FROM rental_requests WHERE id = ?', (request_id,))
                request = cursor.fetchone()
                if request:
                    book_id = request[0]

                    cursor.execute('SELECT COUNT(*) FROM rental_requests WHERE book_id = ? AND is_approved = 1', (book_id,))
                    approved_requests = cursor.fetchone()[0]

                    if approved_requests == 0:
                        cursor.execute('UPDATE books SET is_rented = 1 WHERE id = ?', (book_id,))
                        cursor.execute('UPDATE rental_requests SET is_approved = 1 WHERE id = ?', (request_id,))
                        conn.commit()
                        messagebox.showinfo("Success", "Request approved")
                    else:
                        messagebox.showerror("Error", "Book is already rented")
                else:
                    messagebox.showerror("Error", "Request ID not found")
            else:
                messagebox.showerror("Error", "Invalid Request ID")

        tk.Button(requests_window, text="Approve Request", command=approve_request).pack(pady=10)

    def view_books(self):
        # Fetch and display all books
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        books_list = "\n".join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Rented: {'Yes' if book[3] else 'No'}" for book in books])

        books_window = tk.Toplevel(self)
        books_window.title("Books List")
        books_window.geometry("400x400")

        tk.Label(books_window, text="Books List", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(books_window, wrap="word", height=15, width=50, padx=10, pady=10)
        text_widget.insert(tk.END, books_list)
        text_widget.pack()

    def view_my_books(self, username):
        # Fetch and display books rented by the user
        cursor.execute('''
            SELECT b.id, b.title, b.author
            FROM rental_requests r
            JOIN books b ON r.book_id = b.id
            WHERE r.username = ? AND r.is_approved = 1
        ''', (username,))
        rented_books = cursor.fetchall()

        rented_books_list = "\n".join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}" for book in rented_books])

        my_books_window = tk.Toplevel(self)
        my_books_window.title("My Books")
        my_books_window.geometry("400x400")

        tk.Label(my_books_window, text="My Books", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(my_books_window, wrap="word", height=15, width=50, padx=10, pady=10)
        text_widget.insert(tk.END, rented_books_list)
        text_widget.pack()

    def view_guests(self):
        # Fetch and display all guests
        cursor.execute('SELECT username FROM users WHERE role = "Guest"')
        guests = cursor.fetchall()

        guests_list = "\n".join([f"Username: {guest[0]}" for guest in guests])

        guests_window = tk.Toplevel(self)
        guests_window.title("Registered Guests")
        guests_window.geometry("300x300")

        tk.Label(guests_window, text="Registered Guests", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(guests_window, wrap="word", height=10, width=30, padx=10, pady=10)
        text_widget.insert(tk.END, guests_list)
        text_widget.pack()

    def view_librarians(self):
        # Fetch and display all librarians
        cursor.execute('SELECT username FROM users WHERE role = "Librarian"')
        librarians = cursor.fetchall()

        librarians_list = "\n".join([f"Username: {librarian[0]}" for librarian in librarians])

        librarians_window = tk.Toplevel(self)
        librarians_window.title("Registered Librarians")
        librarians_window.geometry("300x300")

        tk.Label(librarians_window, text="Registered Librarians", font=("Arial", 16)).pack(pady=10)
        text_widget = tk.Text(librarians_window, wrap="word", height=10, width=30, padx=10, pady=10)
        text_widget.insert(tk.END, librarians_list)
        text_widget.pack()

    def logout(self):
        # Hide current frame and show login frame
        if hasattr(self, 'guest_frame'):
            self.guest_frame.pack_forget()
        if hasattr(self, 'librarian_frame'):
            self.librarian_frame.pack_forget()
        self.create_login_widgets()  # Recreate login widgets

