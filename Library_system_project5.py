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

class Book:
    def __init__(self, name:str, id:int, total_quantity:int):
        self.name = name
        self.id = id
        self.total_quantity = total_quantity
        self.total_borrowed = 0

    def borrow(self):
        # checks if there are left books to borrow or not 
        # simply checks its quantity that is in the library now only 
        if self.total_quantity - self.total_borrowed == 0:
            return False
        self.total_borrowed += 1
        return True
     
    def return_copy(self):
        #returning the borrowed book back
        #which is a copy of it
        assert self.total_borrowed > 0
        self.total_borrowed -= 1
    
    def __repr__(self):
        return f"Book name: {self.name:20} - id: {self.id} - total quantity: {self.total_quantity} -"\
                f"total borrowed: {self.total_borrowed}"


class User:
    def __init__(self, name:str, id:int):
        self.name = name
        self.id = id
        self.borrowed_books = {}

    def borrow(self, book:str):
        # storing using book.id as the key
        self.borrowed_books[book.id] = book
    
    def has_borrowed(self, book:str):
        #checks if this user has borrowed this book or not
        return book.id in self.borrowed_books
    
    def return_book(self, book:str):
        #if this book is borrowed it returns it and deletes a copy of it from the list of the borrowed
        if book.id in self.borrowed_books:
            del self.borrowed_books[book.id]

    def simple_repr(self, is_detailed = False):
        ret = f"User name: {self.name:15} - id: {self.id}"
        if is_detailed and self.borrowed_books:
            ret += "\n\tBorrowed Books\n"
            for book in self.borrowed_books.values():
                ret += f"\t{str(book)}\n"
        return ret
        

    def __repr__(self):
        return self.simple_repr(True)    




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
                
    

class FrontEnd:

    def __init__(self):
        self.backend = BackEnd()
        self.dummy_data()
        self.backend.load_from_file()

    def menu(self):
        print("Program Options: ")
        msg = ["Add a Book",
               "Print all library books",
               "Print books by prefix",
               "Add user",
               "Borrow book",
               "Return book",
               "print users borrowed books",
               "print all users",
               "Exit"]

        for idx, option in enumerate(msg):
            print(f"{idx+1}) {option}")   
        choice = valid_int_input(f"Please enter a number between 1 and {len(msg)}: ", 1, len(msg))
        return choice
    
    def dummy_data(self):
            self.backend.add_book('math4', '100', 3)
            self.backend.add_book('math2', '101', 5)
            self.backend.add_book('math1', '102', 4)
            self.backend.add_book('math3', '103', 2)
            self.backend.add_book('prog1', '201', 3)
            self.backend.add_book('prog2', '202', 3)

            self.backend.add_user('mostafa', '30301')
            self.backend.add_user('ali', '50501')
            self.backend.add_user('noha', '70701')
            self.backend.add_user('ashraf', '90901')

            self.backend.borrow_book('mostafa', 'math3')
            self.backend.borrow_book('noha', 'math3')

        
    def run(self):
        while True:
            choice = self.menu()

            if choice == 1:
                self.add_book()
            
            if choice == 2:
                self.print_books()
            
            if choice == 3:
                self.print_name_prefix()
            
            if choice == 4:
                self.add_user()

            if choice == 5:
                self.borrow_book()
            
            if choice == 6:
                self.return_book()

            if choice == 7:
                self.print_users_borrowed_books()

            if choice == 8:
                self.print_users()
            
            if choice == 9:
                self.backend.save_to_file() #save before closing
                print("Program Ended.")
                break
        
    def add_book(self):
        print("\n Enter book info:")
        name = input("Enter book name: ")
        id = input("Enter book id: ")
        total_quantity = valid_int_input(input("Enter quantity of the book: "))
        self.backend.add_book(name, id, total_quantity)

    def print_books(self):
        self.print_name_prefix(just_print_all = True)

    def print_name_prefix(self, just_print_all = False):
        prefix = ""
        if not just_print_all:
            prefix = input("Enter prefix of the book: ")
        books = self.backend.print_by_prefix(prefix)
        book_str = print("\n".join(str(book) for book in books))
        
        return book_str

    def add_user(self):
        print("\nEnter user info:")
        name = input("Enter user name: ")
        id = input("Enter id: ")
        self.backend.add_user(name, id)

    def read_user_name_and_book_name(self, trials = 3):
        """
        this function tries to read valid username and password up to #trials
        If finally correct, it returns the ead names, otherwise None, None
        """
        trials += 1

        while trials > 0:
            trials -= 1
            print("Enter username and book name")

            user_name = input("Enter username: ")
            if self.backend.get_user_by_name(user_name) is None:
                print("Invalid user name!")
                continue
            book_name = input("Enter book name: ")
            if self.backend.get_book_by_name(book_name) is None:
                print("Invalid book name!")
                continue
            return user_name, book_name
        
        print("You did several trials try later!")
        return None, None
            

    def borrow_book(self):
        user_name, book_name = self.read_user_name_and_book_name()

        if user_name is None or book_name is None:
            return
        
        if not self.backend.borrow_book(user_name, book_name):
            print("Failed to borrow book")

    def return_book(self):
        user_name, book_name = self.read_user_name_and_book_name()

        if user_name is None or book_name is None:
            return 
        
        self.backend.return_book(user_name, book_name)

    def print_users_borrowed_books(self):
        book_name = input("Enter book name: ")
        if self.backend.users_borrowed_books(book_name) is None:
            print("Invalid book name!")
        else:
            user_lst = self.backend.users_borrowed_books(book_name)
            if not user_lst:
                print("No one borrowed this book!")
            else:
                print("\nList of users borrowed this book: ")
                for user in user_lst:
                    print(user.simple_repr())

    def print_users(self):
        print("\n--- Library Users ---")
        for user in self.backend.get_all_users():
            #Frontend doesn't know it's a dictionary so don't use
            #XX for user in self.backend.users.values() XX
            print(user) #automatically calls the __repr__ func
       
        

if __name__ == "__main__":
    app = FrontEnd()
    app.run()


"""
 using dictionaries is more better as the seacrch complexity will become O(1)
 the list will make the worst case O(n)
 and that is bad for big system libraries

"""

"""
What is vars as shown in saving the file?
-->In the context of the saving function,
vars() is a built-in Python function that returns the __dict__ attribute of an object.
Essentially, it takes a complex class instance
(like Book or User objects) and turns it into a standard Python dictionary
where the keys are the attribute names and the values are their current data.

Why we use it for saving?
-->The json module only knows how to handle basic data types like
strings, integers, lists, and dictionaries
It has no idea what a Book object is. By using vars(book)
we convert the object into a format that the JSON library can understand and write to a text file.

"""

"""
CIRCULAR REFERENCE: In your specific project, User objects contain a dictionary of Book objects.
If you tried to use vars() on a User directly, it would crash or create a mess
because it would try to save the entire Book object inside the User data.

That's why when i saved the code, i used the vars(user)
but specifically replaced the borrowed_books with just a list of names/IDs.
"""

"""
IOError Occurs When
-->Attempting to open a file that does not exist
-->Trying to write to a file on a full disk
-->Finding problems with file permissions that prevent reading or writing a file
-->Having issues with accessing a device or network resource
"""