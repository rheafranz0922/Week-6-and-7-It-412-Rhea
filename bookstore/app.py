""" 
Bookstore 
Provides a CLI interface to manage the books in bookstore.
"""

# Fixed imports for package
from bookstore.app import add_book, remove_book, record_sale, db
from bookstore.database import Database
from bookstore.models import Book
from bookstore.validators import (
    validate_title,
    validate_author,
    validate_quantity,
    validate_signed,
    validate_price
)
# Create a database instance and load of existing the inventory from CSV
db = Database()
db.load_from_csv()


def display_books():
    """Display all of the books currently was stored in database."""
    books = db.get_all()

    """If no books was exist, notify the user"""
    if not books:
        print("Books are not available.")
        return

    print("\nBook Inventory:")
    print("-" * 70)

     # Loop will display the books in details.
    for book in books:
        print(f"ID: {book.book_id}")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Quantity: {book.quantity}")
        print(f"Signed: {'Yes' if book.signed == 'Y' else 'No'}")
        print(f"Promo Price: {book.promo_price if book.promo_price is not None else 'N/A'}")
        print(f"Retail Price: {book.retail_price}")
        print("-" * 70)


def add_book():
    title = input("Enter book title: ").strip()
    while not validate_title(title):
        title = input("Invalid title. Enter book title: ").strip()

    # Validate of the Author
    author = input("Enter book author: ").strip()
    while not validate_author(author):
        author = input("Invalid author. Enter book author: ").strip()
    
    # Validate quantity
    quantity = input("Enter quantity: ").strip()
    while not validate_quantity(quantity):
        quantity = input("Invalid quantity. Enter quantity: ").strip()
    quantity = int(quantity)

    # Optiona signed from validate
    signed = input("Is it a signed edition? (Y/N, leave blank if no): ").strip()
    while not validate_signed(signed):
        signed = input("Invalid input. Is it signed? (Y/N, leave blank if no): ").strip()
    signed = signed.upper() if signed.upper() == "Y" else ""

    # the PROMO PRICE
    promo_price = input("Enter promotional price (leave blank if none): ").strip()
    if promo_price == "":
        promo_price = None
    else:
        while not validate_price(promo_price):
            promo_price = input("Invalid price. Enter promotional price: ").strip()
        promo_price = float(promo_price)
    
    #Validate the retail price.
    retail_price = input("Enter retail price: ").strip()
    while not validate_price(retail_price):
        retail_price = input("Invalid price. Enter retail price: ").strip()
    retail_price = float(retail_price)

    #Create the book object
    book = Book(
        title=title,
        author=author,
        quantity=quantity,
        signed=signed,
        promo_price=promo_price,
        retail_price=retail_price,
    )

    # Add book from the database and save the CSV.
    db.add(book)
    db.export_to_csv()
    print(f"Book '{title}' added successfully!")


def remove_book():
    book_id = input("Enter the Book ID to remove: ").strip()
    book = db.get_by_id(book_id)

    if not book:
        print("Book ID not found.")
        return
    
    #Confirm in delete
    confirm = input(f"Are you sure you want to delete '{book.title}'? (Y/N): ").strip().upper()

    if confirm == "Y":
        db.remove(book_id)
        db.export_to_csv()
        print("Book removed successfully.")
    else:
        print("Operation cancelled.")


def record_sale():
    #Ask for the Book ID
    book_id = input("Enter the Book ID was sold: ").strip()
    book = db.get_by_id(book_id)

    #Check if the book was exist
    if not book:
        print("Book was not found.")
        return
    
    #Get the validate of quantity
    sold_qty = input("Enter quantity sold: ").strip()
    while not validate_quantity(sold_qty):
        sold_qty = input("Invalid quantity. Enter quantity sold: ").strip()
    sold_qty = int(sold_qty)

    #Update the quantity and save it.
    if sold_qty > book.quantity:
        print(f"Cannot sell {sold_qty}  the copies. Only {book.quantity} available.")
        return

    book.quantity -= sold_qty
    db.export_to_csv()
    print(f"Sale recorded. Remaining quantity: {book.quantity}")

#Edit the details of the book.
def edit_book():
    book_id = input("Enter Book ID to edit: ").strip()
    book = db.get_by_id(book_id)

    if not book:
        print("Book ID not found.")
        return
    
    #Display  and select the editable menu from the bookstore.
    print("Select field to edit:")
    print("1. Title")
    print("2. Author")
    print("3. Quantity")
    print("4. Signed")
    print("5. Promotional Price")
    print("6. Retail Price")

    choice = input("Enter your choices (1-6): ").strip()

    if choice == "1":
        value = input("Enter new title: ").strip()
        while not validate_title(value):
            value = input("Invalid title. Enter new title: ").strip()
        book.title = value

    elif choice == "2":
        value = input("Enter new author: ").strip()
        while not validate_author(value):
            value = input("Invalid author. Enter new author: ").strip()
        book.author = value

    elif choice == "3":
        value = input("Enter new quantity: ").strip()
        while not validate_quantity(value):
            value = input("Invalid quantity. Enter new quantity: ").strip()
        book.quantity = int(value)

    elif choice == "4":
        value = input("Is it signed? (Y/N, leave blank if no): ").strip()
        while not validate_signed(value):
            value = input("Invalid input. Is it signed? (Y/N, leave blank if no): ").strip()
        book.signed = value.upper() if value.upper() == "Y" else ""

    elif choice == "5":
        value = input("Enter new promotional price (leave blank if none): ").strip()
        if value == "":
            book.promo_price = None
        else:
            while not validate_price(value):
                value = input("Invalid price. Enter new promotional price: ").strip()
            book.promo_price = float(value)

    elif choice == "6":
        value = input("Enter new retail price: ").strip()
        while not validate_price(value):
            value = input("Invalid price. Enter new retail price: ").strip()
        book.retail_price = float(value)

    else:
        print("Invalid choice.")
        return
    
    #Save the changes of the book.
    db.export_to_csv()
    print("Book updated successfully.")


def main_menu():
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. Show all books")
        print("2. Add a book")
        print("3. Record a book sale")
        print("4. Edit book details")
        print("5. Remove a book")
        print("6. Exit (Save & Generate CSV)")

        choice = input("Enter your choice (1-6): ").strip()

        #Corresponding function
        if choice == "1":
            display_books()

        elif choice == "2":
            add_book()

        elif choice == "3":
            record_sale()

        elif choice == "4":
            edit_book()

        elif choice == "5":
            remove_book()

        elif choice == "6":
            db.export_to_csv()
            print("\nInventory saved successfully.")
            print("Exiting program. Goodbye Thank you!")
            break

        else:
            print("Invalid choice. Please select  the number1-6.")

# Run progrsm
if __name__ == "__main__":
    main_menu()