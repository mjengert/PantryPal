from item import Item


class Pantry_List:
    def __init__(self):
        self.items = {}

    def addToPantry(self, item):
        self.items[item.getName()] = item

    def removePantry(self, item):
        del self.items[item.getName()]

    def display(self):
        """Display all pantry items."""
        if not self.items:
            print("Your pantry is empty.")
            return
        for item in self.items:
            print(f"{item}")

    def getRange(self):
        return self.items.__len__()

    def getItem(self, index):
        return self.items[index]
    def getItems(self):
        return self.items
    def getExpiration(self, index):
        return self.items[index].getExpiration()

