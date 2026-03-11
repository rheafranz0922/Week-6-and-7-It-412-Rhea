"""
Book Data Model
It Contains the book class with all required attributes.
"""
from dataclasses import dataclass, field
import uuid

@dataclass
class Book:

    # Title of the book
    title: str

    # The name of the book's author
    author: str

    #Number of copies available in stock
    quantity: int

    #Regular selling the price of the book
    retail_price: float

    #Indicates if the book is signed.
    signed: str = ""

    #Promotional from discount the price of the book
    promo_price: float = None

    #Unique identifier from the each book. Automatically to generates the UUID String was not provided
    book_id: str = field(default_factory=lambda: str(uuid.uuid4()))