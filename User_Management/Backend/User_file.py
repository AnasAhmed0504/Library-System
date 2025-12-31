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
