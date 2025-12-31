from Backend.Backend_file import BackEnd, valid_int_input

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
