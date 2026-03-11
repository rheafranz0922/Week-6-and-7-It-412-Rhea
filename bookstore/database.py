"""
Database Module
Contains the book for class with all required the attributes.
"""
import os
import csv
from mysql.connector import Error
from models import Book

class Database:
    """A simple in-memory database for storing books."""

    def __init__(self):
        #Create an empty list to store the book objects.
        self._books = []

    def load_from_csv(self, filename="export.csv"):
        #Get directory where this file was located.
        base_dir = os.path.dirname(os.path.abspath(__file__))

        #Create the full filepath
        filepath = os.path.join(base_dir, filename)

        #If CSV file doest not exist, it will stop loading.
        if not os.path.exists(filepath):
            return

        with open(filepath, mode="r", newline="") as file:
            reader = csv.reader(file)

            #Skip the header row instead I put reader in row
            next(reader, None)

            #Read each row from CSV file, and Ensure the row has the correct number of columns
            for row in reader:
                if len(row) != 7:
                    continue

                #Create book objects using the row data, convert the quantity of integerr, 
                #promo price or set, and retail price from float.
                book = Book(
                    title=row[1],
                    author=row[2],
                    quantity=int(row[3]),
                    signed=row[4],
                    promo_price=float(row[5]) if row[5] else None,
                    retail_price=float(row[6]),
                    book_id=row[0],
                )

                #Add the book to the in-memory list.
                self._books.append(book)

    def add(self, book):
        #Add a new book object from the database.
        self._books.append(book)

    def remove(self, book_id):
        #Remove a book from database using the ID and create a new list excluding the matching book.
        self._books = [b for b in self._books if b.book_id != book_id]

    def get_all(self):
        #Return the list of all the books
        return self._books

    def get_by_id(self, book_id):
        #Search a book by using the ID
        for book in self._books:
            if book.book_id == book_id:
                return book # Return the book if the book was found.
        return None #Return None if not found

    def export_to_csv(self, filename="export.csv"):
        # Get the directory where this file is located.
        base_dir = os.path.dirname(os.path.abspath(__file__))

        #Create the full filepath
        filepath = os.path.join(base_dir, filename)

        #Open the CSV file in write mode.
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)

            #Write the header row
            writer.writerow(
                ["ID", "Title", "Author", "Quantity", "Signed", "Promo Price", "Retail Price"]
            )

            # Write the book's data from the CSV file
            for book in self._books:
                writer.writerow([
                    book.book_id,
                    book.title,
                    book.author,
                    book.quantity,
                    book.signed,
                    book.promo_price,
                    book.retail_price,
                ])

   