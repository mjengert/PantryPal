from pantryList import Pantry_List
from groceryList import Grocery_List
class User:
    def __init__(self, username, password, name, email, location, groceryList, pantryList):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.location  = location
        self.pantry =Pantry_List()
        self.grocery = Grocery_List()

    def add_to_grocery(self, item_name):
        """User adds an item to their grocery list."""
        self.grocery_list.add_item(item_name)

    def check_off_grocery_item(self, item_name):
        """User checks off an item, moving it from grocery to pantry."""
        self.grocery_list.check_off_item(item_name, self.pantry_list)

    def view_pantry_list(self):
        """User views their pantry list."""
        self.pantry_list.display()