import pytest
from unittest.mock import patch
from bookstore.app import main_menu

def test_main_menu_exit(capsys):
    """
    Test the main menu to display an exit the option 6.
    """

    # Mock the user input to choose the exit.
    with patch("builtins.input", side_effect=["6"]):
        main_menu()

    # Capture the printed output
    captured = capsys.readouterr()
    output = captured.out

    # Check the menu if it was appear.
    assert "--- Bookstore Menu ---" in output
    assert "1. Show all books" in output
    assert "6. Exit (Save & Generate CSV)" in output

    # Check exit.
    assert "Inventory saved successfully." in output
    assert "Exiting program. Goodbye!" in output