
from datetime import datetime, timedelta

# Dictionary mapping categories to expiration times
food_expiration = {
    "Meat": ["beef", "pork", "lamb", "veal", "steak", "sirloin", "ribeye", "pork chops"],
    "Ground Meat": ["ground beef", "ground pork", "ground chicken", "ground turkey"],
    "Poultry": ["chicken", "turkey", "duck", "chicken thighs", "turkey leg", "chicken breast", "chicken wings"],
    "Fish": ["fish", "salmon", "tuna", "cod", "tilapia", "catfish"],
    "Cooked Meats": ["cooked beef", "cooked chicken", "cooked pork", "cooked turkey","lunch meat", "ham", "roast beef", "turkey slices", "deli meat", "sliced meat",
                     "sliced chicken", "deli chicken", "deli turkey"],
    "Eggs": ["eggs"],
    "Milk": ["milk", "butter", "yogurt", "cream", "half and half","cheese"],
    "Fruits": [
        "banana", "apple", "grape", "strawberry", "blueberry", "raspberry", 
        "orange", "avocado", "melon", "pear", "lemon", "lime", "peach", "pineapple"
    ],
    "Vegetables": [
        "potato", "tomato", "lettuce", "carrot", "onion", "cucumber", 
        "pepper", "broccoli", "celery", "spinach", "squash"
    ],"Grains": ["rice", "pasta", "oats", "quinoa", "barley", "cereal"],
    "Bread": ["bread"]
}

expiration_times = {
    "Meat": 5,
    "Ground Meat": 2,
    "Poultry": 2,
    "Fish": 2,
    "Cooked Meats": 5,
    "Eggs": 35,  
    "Milk": 7,
    "Fruits": 7,  
    "Vegetables": 7,
    "Grains": 180,
    "Bread": 7
}
class Item:
    def __init__(self, name):
        self.name = name.lower()
        self.itemType = self.findType()
        self.expiration = ""
    
    #Get grocery type from list
    def findType(self):
        itemCat="Unknown"
        for category, items in food_expiration.items():
            for item in items:
                if item in self.name:
                    itemCat = category

        return itemCat
    
    def getName(self):
        return self.name

    def getType(self):
        return self.itemType
    #return expiration date
    def getExpiration(self):
        if (self.expiration):
            return f"Expires {self.expiration}"

        return " "
    
    #Get expiration date from list   
    def calcExpiration(self):
        if self.itemType in expiration_times:
            days_until_expire = expiration_times[self.itemType]
            expiration_date = datetime.today() + timedelta(days=days_until_expire)
            self.expiration = expiration_date.strftime("%m-%d-%Y")
        return "N/A"
