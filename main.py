from app import LibraryApp
from database import setup_database

if __name__ == "__main__":
    setup_database()
    app = LibraryApp()
    app.mainloop()
