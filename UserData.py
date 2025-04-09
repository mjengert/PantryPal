from pymongo import MongoClient

def getUserData(username):

    uri = ""
    client = MongoClient(uri)
    database = client.get_database("userInformation")
    collection = database.get_collection("StarterProfiles")
    # Query for a movie that has the title 'Back to the Future'
    query = { "username": username }
    user = collection.find_one(query)
    client.close()
    return user