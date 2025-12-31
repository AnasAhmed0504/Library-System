from Book_Management.Book_file import Book
from User_Management.User_file import User
import json


#Class Exceptions for better Error Tracking
class LibraryError(Exception): pass #Base class for Library exceptions
class BookNotFoundError(LibraryError):pass #Raised when book doesn't exist
class UserNotFoundError(LibraryError):pass #Raised when user doesn't exist
class OutOfStockError(LibraryError): pass #Raised when no copies are available

def valid_int_input(msg, start = 0, end = None):
    while True:
        try:
            user_input = int(input(msg))
            if (start is not None and user_input < start) or (end is not None and user_input > end):
                print(f"Please enter an integer between {start} and {end}.")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
class BackEnd:
    """
    This backend
    -->Handles the business logic for the Book and User management
    -->saves the file data
    """
    def __init__(self):
        #storing books/users in dictionaries: {name: object}
        self.books = {}
        self.users = {}

    # ---Getters (Encapsulation) ---   
     
    def get_all_users(self):
        return self.users.values()
    
    def get_user_by_name(self, name:str):
        return self.users.get(name)
    
    def get_book_by_name(self, name:str):
        return self.books.get(name)

    # --- Bussiness Logic --- 

    def add_book(self, name:str, id:int, total_quantity:int):
        if name in self.books:
            print(f"Book '{name}' already exists, updating quantity")
            self.books[name].total_quantity += total_quantity
        else:
            self.books[name] = Book(name, id, total_quantity)
    
    def print_by_prefix(self, prefix:str):
        return [book for name, book in self.books.items() if name.startswith(prefix)]

    def add_user(self, name:str, id:int):
        if name in self.users:
            print(f"User '{name}' already exists.")
            return False
        self.users[name] = User(name, id)
        return True

    
    
    def borrow_book(self, user_name:str, book_name:str):
        """
        Attempts to link a book to a user.
        Returns True if successful, False if book is unavailable or user not found.
        """
        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if not user:
            raise UserNotFoundError(f"User {user_name} is not Found")
        if not book:
            raise BookNotFoundError(f"Book {book_name} is not Found")
        
        if book.borrow():
            user.borrow(book)
            return True
        raise OutOfStockError(f"'{book_name}' is currently out of stock.")    
    
    def return_book(self, user_name:str, book_name:str):

        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if user is None or book is None:
            return
        
        if user.has_borrowed(book):
            user.return_book(book)
            book.return_copy()
        else: 
            print("This user did not borrow this book")

    
    def users_borrowed_books(self, book_name:str): 
        book = self.get_book_by_name(book_name)

        if book is None:
            return []
        return [user for user in self.users.values() if user.has_borrowed(book)]
    
    
    #--- Persistence (Clean File I/O) ---

    def save_to_file(self, filename = "Library_data.json"):
        data = {
            "books": [vars(book) for book in self.books.values()],
            "users": []
        }

        for user in self.users.values():
            user_data = vars(user).copy()
            #Convert borrowed books objects back to just names/IDs
            #To avoid circular reference
            user_data["borrowed_books"] = [book.name for book in user.borrowed_books.values()]
            data["users"].append(user_data)

        #opening the file mustn't be inside a loop
        #open the file once, write or read everything, then close it
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent = 4)
            print("Data saved succesfully")

        except IOError as e:
            #raised when an input/output operation fails
            print(f"Failed to save data: {e}")
    
    def load_from_file(self, filename = "Library_data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Reconstruct Books
            self.books = {}
            for b_data in data["books"]:
                book = Book(b_data["name"], b_data["id"], b_data["total_quantity"])
                book.total_borrowed = b_data["total_borrowed"]
                self.books[book.name] = book
                #book's name is the key

            # Reconstruct Users
            self.users = {}
            for u_data in data["users"]:
                user = User(u_data["name"], u_data["id"])
                # Re-link borrowed books by finding the book objects by name
                for b_name in u_data.get("borrowed_books", []):
                    if b_name in self.books:
                        # Use User.borrow to keep mapping consistent (id -> Book)
                        user.borrow(self.books[b_name])
                self.users[user.name] = user
                #user's name is the key 


        except FileNotFoundError:
            print("No saved data found, Starting Fresh.")
