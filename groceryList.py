from item import Item
from pantryList import Pantry_List
class Grocery_List:
    def __init__(self):
        self.items = []

    def addToGrocery(self,item):
        self.items.append(item)
    
    def removeGrocery(self,item):
        self.items.remove(item)
    
    def checkOff(self,item, pantryList):
        self.items.remove(item)
        pantryList.addToPantry(item)