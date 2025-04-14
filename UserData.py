import pymongo
from item import Item
from groceryList import Grocery_List
from pantryList import Pantry_List
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from dateutil import parser

class UserData:

    def __init__(self, username):
        self.user = self.getUserData(username)
        self.username = self.user["username"]
        self.grocery = Grocery_List()
        self.pantry = Pantry_List()

        for item in self.user["grocery_list"]:
            item_name = item.get("name")
            item_exp = item.get("exp")
            exp_str = item_exp.strftime("%m/%d/%Y")
            groc_item = Item(item_name, exp_str)
            self.grocery.addToGrocery(groc_item)

        for item in self.user["pantry_list"]:
            item_name = item.get("name")
            item_exp = item.get("exp")
            exp_str = item_exp.strftime("%m/%d/%Y")
            pan_item = Item(item_name, exp_str)
            self.pantry.addToPantry(pan_item)


    def getUserData(self, username):
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        client = MongoClient(uri)
        database = client.get_database("userInformation")
        collection = database.get_collection("StarterProfiles")
        query = { "username": username }
        user = collection.find_one(query)
        #print(user)
        #client.close()
        return user

    def getPantryList(self):
        return self.pantry

    def getGroceryList(self):
        return self.grocery

    def addToGrocDB(self, item):
        new_item = {
            "name": item.getName(),
            "exp": item.getExpiration()
        }
        self.user["grocery_list"].insert_one(new_item)

    def addToPantryDB(self, item):
        new_item = {
            "name": item.getName(),
            "exp": item.getExpiration()
        }
        self.user["pantry_list"].insert_one(new_item)

    #def delFromGrocDB(self, item):


    #def delFromPantryDB(self, item):