from item import Item
from pantryList import Pantry_List
class Grocery_List:
    def __init__(self):
        self.items = [Item('Apples'), Item('Bananas'), Item('Oranges'), Item('Milk')]

    def addToGrocery(self,item):
        self.items.append(item)
    
    def removeGrocery(self,item):
        self.items.remove(item)
    
    def checkOff(self,item, pantryList):
        self.items.remove(item)
        pantryList.addToPantry(item)

    def getItem(self, index):
        return self.items[index]

    def getRange(self):
        return len(self.items)