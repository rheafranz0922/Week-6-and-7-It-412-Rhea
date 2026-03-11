"""
Validators Module
contains a functions to validate the book attributes from the bookstore project.
"""
import re


def validate_title(title: str) -> bool:
    """Validate book title."""
    return isinstance(title, str) and title.strip() != ""


def validate_author(author: str) -> bool:
    """Validate author name."""
    if not isinstance(author, str) or author.strip() == "":
        return False

    pattern = r"^[A-Za-z ,.'-]+$"
    return bool(re.match(pattern, author.strip()))


def validate_quantity(quantity: str) -> bool:
    """Validate integer quantity."""
    try:
        return int(quantity) >= 0
    except (ValueError, TypeError):
        return False


def validate_signed(value: str) -> bool:
    """Validate signed field  using Y, N, or blank."""
    if value is None or value.strip() == "":
        return True
    return value.upper() in ("Y", "N")


def validate_price(price: str) -> bool:
    """Validate price from float."""
    try:
        return float(price) >= 0
    except (ValueError, TypeError):
        return False