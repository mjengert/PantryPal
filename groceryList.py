from item import Item
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView


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



