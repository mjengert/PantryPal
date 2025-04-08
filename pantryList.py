from item import Item


class Pantry_List:
    def __init__(self):
        self.items = []
    
    def addToPantry(self,item):
        self.items.append(item)
    
    def removePantry(self,item):
        self.items.remove(item)
    
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

    def getExpiration(self, index):
        return self.items[index].getExpiration()