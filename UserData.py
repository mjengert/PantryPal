import pymongo
import logging
from item import Item
from groceryList import Grocery_List
from pantryList import Pantry_List
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class UserData:

    def __init__(self, username):
        user = self.getUserData(username)
        self.username = user["username"]
        self.grocery = Grocery_List()
        self.pantry = Pantry_List()

        for item in user["grocery_list"]:
            groc_item = Item(item)
            self.grocery.addToGrocery(groc_item)

        for item in user["pantry_list"]:
            pan_item = Item(item)
            self.pantry.addToPantry(pan_item)


    def getUserData(self, username):
        #uri = "mongodb+srv://rbaryol:JTreeQDIPNgjvKP6@cluster0.wgradsb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        load_dotenv()
        uri = os.getenv("MONGODB_URI")
        client = MongoClient(uri)
        database = client.get_database("userInformation")
        collection = database.get_collection("StarterProfiles")
        # Query for a movie that has the title 'Back to the Future'
        query = { "username": username }
        user = collection.find_one(query)
        print(user)
        client.close()
        return user

    def getPantryList(self):
        return self.pantry

    def getGroceryList(self):
        return self.grocery