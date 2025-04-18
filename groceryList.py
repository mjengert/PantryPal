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

    def getItem(self, index):
        return self.items[index]

    def getRange(self):
        return len(self.items)

    def getItemFromStr(self, str):
        for item in self.items:
            if item.name == str:
                return item