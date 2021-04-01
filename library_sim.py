class LibraryItem:
    """Class that initializes library items and logs item information"""

    def __init__(self, library_item_id, title):
        """Initializes parameters for class LibraryItem"""
        self._library_item_id = library_item_id
        self._title = title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = None

    def get_library_item_id(self):
        """Allows for retrieval of item ID."""
        return self._library_item_id

    def get_title(self):
        """Allows for retrieval of item title"""
        return self._title

    def set_library_item_id(self, library_item_id):
        """Initializes the id code of an item"""
        self._library_item_id = library_item_id

    def get_location(self):
        """Allows for retrieval of item location."""
        return self._location

    def set_location(self, location):
        """Initializes location of library items."""
        self._location = location

    def get_checked_out_by(self):
        """Allows for retrieval of patron that checked out library item"""
        return self._checked_out_by

    def set_checked_out_by(self, patron):
        """Initializes who checks out library item"""
        self._checked_out_by = patron

    def get_requested_by(self):
        """Allows for retrieval of who requested  an item."""
        return self._requested_by

    def set_requested_by(self, patron):
        """Initializes who requests a library item"""
        self._requested_by = patron

    def get_date_checked_out(self):
        """Allows for retrieval of the date library item was checked out"""
        return self._date_checked_out

    def set_date_checked_out(self, date_checked_out):
        """Initializes the date library item was checked out"""
        self._date_checked_out = date_checked_out


class Book(LibraryItem):
    """Class inherits item ID and title from Library class, keeps track of book items."""

    def __init__(self, library_item_id, title, author):
        """Inherits the id code and title from the parent(super) class."""
        super().__init__(library_item_id, title)
        self._author = author

    def get_author(self):
        """Allows for retrieval of book author"""
        return self._author

    def get_check_out_length(self):
        """Allows for retrieval of the number of days a Book may be checked out for."""
        return 21


class Album(LibraryItem):
    """Class inherits item ID and title from Library class, keeps track of album items."""

    def __init__(self, library_item_id, title, artist):
        """Inherits the id code and title from the parent(super) class."""
        super().__init__(library_item_id, title)
        self._artist = artist

    def get_artist(self):
        """Allows for retrieval of the artist of the Album."""
        return self._artist

    def get_check_out_length(self):
        """Allows for retrieval of the number of days an Album may be checked out for."""
        return 14


class Movie(LibraryItem):
    """Class inherits item ID and title from Library class, keeps track of movie items."""

    def __init__(self, library_item_id, title, director):
        """Inherits the id code and title from the parent(super) class."""
        super().__init__(library_item_id, title)
        self._director = director

    def get_director(self):
        """Allows for retrieval of the director of the Movie."""
        return self._director

    def get_check_out_length(self):
        """Allows for retrieval of the number of days a Movie may be checked out for."""
        return 7


class Patron:
    """Creates class for all actions a library Patron can perform."""

    def __init__(self, patron_id, name):
        """Initializes patron ID, name, and fines at 0, and creates empty list for checked out items."""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = {}  # Utilize dictionary to organize checked out items
        self._fine_amount = 0.00

    def get_patron_id(self):
        """Allows for retrieval of patron ID."""
        return self._patron_id

    def get_name(self):
        """Allows for retrieval of patron name."""
        return self._name

    def get_checked_out_items(self):
        """Allows for retrieval of list of checked out items."""
        return self._checked_out_items

    def set_fine_amount(self, fine):
        """Initializes fine amount as fine."""
        self._fine_amount = fine

    def get_fine_amount(self):
        """Allows for retrieval of patron's accumulated total amount of fines."""
        return self._fine_amount

    def add_library_item(self, library_item):
        """Adds library items to checkout cart."""
        self._checked_out_items[library_item.get_library_item_id()] = library_item

    def remove_library_item(self, library_item):
        """Removes library items to checkout cart."""
        if library_item.get_library_item_id() in self._checked_out_items:
            self._checked_out_items.pop(library_item.get_library_item_id())

    def amend_fine(self, fine_amount):
        """Raises or lowers fine amount depending on Patron actions."""
        self._fine_amount = self._fine_amount + fine_amount


class Library:
    """Tracks all happenings within Library system."""

    def __init__(self):
        """Initializes holdings and members as empty lists and the current date as 0."""
        self._holdings = {}  # Dictionary to organize library  holdings
        self._members = {}  # Dictionary to organize library members
        self._current_date = 0

    def get_holdings(self):
        """Allows for retrieval for holdings."""
        return self._holdings

    def get_members(self):
        """Allows for retrieval of library members"""
        return self._members

    def add_library_item(self, library_item):
        """Adds library items to holdings list."""
        self._holdings[library_item.get_library_item_id()] = library_item

    def add_patron(self, patron):
        """Adds patron to members list."""
        self._members[patron.get_patron_id()] = patron

    def get_library_item_from_id(self, library_item_id):
        """Allows retrieval of library item from library item's ID."""
        if library_item_id in self._holdings:
            return self._holdings[library_item_id]
        else:
            return None

    def get_patron_from_id(self, patron_id):
        """Allows for retrieval of patron name using their patron ID."""
        if patron_id in self._members:
            return self._members[patron_id]
        else:
            return None

    def check_out_library_item(self, patron_id, library_item_id):
        """Checks that item is available for check out."""
        patron = self.get_patron_from_id(patron_id)
        if patron is None:
            return "patron not found"

        library_item = self.get_library_item_from_id(library_item_id)
        if library_item is None:
            return "item not found"

        if library_item.get_location() == "CHECKED_OUT":
            return "item already checked out"
        elif library_item.get_location() == "ON_HOLD_SHELF" and library_item.get_requested_by().get_patron_id() \
                != patron_id:
            return "item on hold by other patron"

        library_item.set_checked_out_by(patron)
        library_item.set_date_checked_out(self._current_date)
        library_item.set_location("CHECKED_OUT")

        requested_by = library_item.get_requested_by()
        if requested_by is not None and requested_by.get_patron_id() == patron_id:
            library_item.requested_by = None
        self._holdings[library_item_id] = library_item
        self._members[patron_id].add_library_item(library_item)
        return "check out successful"

    def return_library_item(self, library_item_id):
        """Makes sure the library item was returned"""
        library_item = self.get_library_item_from_id(library_item_id)
        if library_item is None:
            return "item not found"

        if library_item.get_location() != "CHECKED_OUT":
            return "item already in library"

        patron = library_item.get_checked_out_by()
        self._members[patron].remove_library_item(library_item)

        requested_by = library_item.get_requested_by()
        if requested_by is not None and requested_by.get_patron_id() != patron.get_patron_id():
            library_item.set_location("ON_HOLD_SHELF")
        else:
            library_item.set_location("ON_SHELF")
        library_item.set_checked_out_by(None)
        self._holdings[library_item_id] = library_item
        return "return successful"

    def request_library_item(self, patron_id, library_item_id):
        """Allows for a library item to be requested."""
        patron = self.get_patron_from_id(patron_id)
        if patron is None:
            return "patron not found"

        library_item = self.get_library_item_from_id(library_item_id)
        if library_item is None:
            return "item not found"

        requested_by = library_item.get_requested_by()
        if requested_by is not None:
            return "item already on hold"

        library_item.set_requested_by(patron)

        if library_item.get_location() == "ON_SHELF":
            library_item.set_location("ON_HOLD_SHELF")

        return "request successful"

    def pay_fine(self, patron_id, amount):
        """Allows for patron to pay fine"""
        patron = self.get_patron_from_id(patron_id)
        if patron is None:
            return "patron not found"

        patron.amend_fine(- amount)
        self._members[patron.get_patron_id()] = patron
        return "payment successful"

    def increment_current_date(self):
        """Increments patron fine by 10 cents for each overdue library item"""
        self._current_date = self._current_date + 1
        for patron_id in self._members:
            patron = self._members[patron_id]
            for library_item_id in patron.get_checked_out_items():
                library_item = patron.get_checked_out_items()[library_item_id]
                if self._current_date - library_item.get_date_checked_out() > library_item.get_check_out_length():
                    patron.amend_fine(0.1)
                    self._members[patron.get_patron_id()] = patron