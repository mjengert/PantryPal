import datetime

import pymongo
from bson import ObjectId

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
        self.username = self.user[0]["username"]
        self.password = self.user[0]["password"]
        self.grocery = Grocery_List()
        self.pantry = Pantry_List()

        for item in self.user[0]["grocery_list"]:
            item_name = item.get("name")
            item_exp = item.get("exp")
            if (isinstance(item_exp, str)):
                exp_str = item_exp
            else:
                exp_str = item_exp.strftime("%m/%d/%Y")
            groc_item = Item(item_name, exp_str)
            self.grocery.addToGrocery(groc_item)

        for item in self.user[0]["pantry_list"]:
            item_name = item.get("name")
            item_exp = item.get("exp")
            if (isinstance(item_exp, str)):
                exp_str = item_exp
            else:
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
        return user, collection

    def getPantryList(self):
        return self.pantry

    def getGroceryList(self):
        return self.grocery

    def getPassword(self):
        return self.password

    def addToGrocDB(self, item):
        name = item.getName()
        exp = datetime.datetime(2025, 4, 30).isoformat()
        collection = self.user[1]
        id = self.user[0]["_id"]
        query_filter = {'_id': id}
        update_operation = {'$push': { 'grocery_list': {"name": name, "exp": exp}}}
        collection.update_one(query_filter, update_operation, upsert=True)

    def addToPantryDB(self, item):
        name = item.getName()
        exp = datetime.datetime(2025, 4, 30).isoformat()
        collection = self.user[1]
        id = self.user[0]["_id"]
        query_filter = {'_id': id}
        update_operation = {'$push': {'pantry_list': {"name": name, "exp": exp}}}
        collection.update_one(query_filter, update_operation, upsert=True)

    def delFromGrocDB(self, item):
        name = item.getName().lower()
        collection = self.user[1]
        id = self.user[0]["_id"]
        query_filter = {'_id': id}
        update_operation = {'$pull': {'grocery_list': {"name": name}}}
        collection.update_one(query_filter, update_operation)

    def delFromPantryDB(self, item):
        name = item.getName().lower()
        collection = self.user[1]
        id = self.user[0]["_id"]
        query_filter = {'_id': id}
        update_operation = {'$pull': {'pantry_list': {"name": name}}}
        collection.update_one(query_filter, update_operation)