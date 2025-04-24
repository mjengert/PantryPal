
class Grocery_List:
    def __init__(self):
        self.items = {}
    def getItems(self):
        return self.items
    def addToGrocery(self, item):
        if item not in self.items:
            self.items[item.getName()] = item

    def removeGrocery(self, item):
        del self.items[item.getName()]

    def checkOff(self, item, pantryList):
        self.removeGrocery(item)
        if item.getName() not in pantryList.items.keys():
            item.calcExpiration()
            pantryList.addToPantry(item)
            return True
        else:
            return False



