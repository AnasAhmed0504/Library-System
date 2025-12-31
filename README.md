# Library-System
#Overview

A high-performance Library Management System built with Python, utilizing Object-Oriented Programming (OOP) and $O(1)$ search complexity through dictionary-based data structures. The system supports persistent data storage via JSON serialization.

#Key Architecture Features

-->Performance Optimized: Replaced list-based searches with hash maps (dictionaries) for constant-time lookups of books and users.

-->Data Persistence: Automatic saving and loading of the library state to prevent data loss between sessions.

-->Robust Error Handling: Implements a custom exception hierarchy (LibraryError, BookNotFoundError, etc.) to manage edge cases gracefully.

#How to use the program

A menu is displayed when you run the program

Press 1 if you want to add a book to the Library, you will be asked for the name of the book, the id of it, you can create one, but be careful if it is already taken by another book, and enter the quantity of this book

Press 2 if you want to know all the books that are in the library right now

Press 3 if you wan to search for a book with a specific prefix instead of writing the whole book name

Press 4 If you want to login in the library system as a user

Press 5 if you want to Borrow a book from the Library, BUT you have to login first and become a user

Press 6 if you want to return a book you already borrowed

Press 7 if you want to see all the users who borrowed books, you can see the User and the book they borrowed

Press 8 if you only want to know all the users

Press 9 to End the Program
