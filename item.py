
from datetime import datetime, timedelta

# Dictionary mapping categories to expiration times
food_expiration = {
    "Meat": ["beef", "pork", "lamb", "veal", "steak"],
    "Ground Meat": ["ground beef", "ground pork", "ground chicken", "ground turkey"],
    "Poultry": ["chicken", "turkey", "duck"],
    "Fish": ["fish", "salmon", "tuna", "cod", "tilapia"],
    "Cooked Meats": ["cooked beef", "cooked chicken", "cooked pork", "cooked turkey","lunch meat", "ham", "roast beef", "turkey slices", "deli meat", "sliced meat"],
    "Eggs": ["eggs"],
    "Milk": ["milk", "butter", "yogurt", "cream", "half and half","cheese"],
    "Fruits": [
        "banana", "apple", "grape", "strawberry", "blueberry", "raspberry", 
        "orange", "avocado", "melon", "pear", "lemon", "lime", "peach", "pineapple"
    ],
    "Vegetables": [
        "potato", "tomato", "lettuce", "carrot", "onion", "cucumber", 
        "pepper", "broccoli", "celery", "spinach", "squash"
    ]
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
    "Vegetables": 7  
}
class Item:
    def __init__(self, name):
        self.name = name.lower()
        self.itemType = self.getType()
        self.expiration = self.getExpiration()
    
    #Get grocery type from list
    def getType(self):
        for category, items in food_expiration.items():
            if self.name in items:
                return category
        return "Unknown"
    
    def getName(self):
        return self.name
    
    #return expiration date
    def getExpiration(self):
        return self.expiration
    
    #Get expiration date from list   
    def calcExpiration(self):
        if self.itemType in expiration_times:
            days_until_expire = expiration_times[self.itemType]
            expiration_date = datetime.today() + timedelta(days=days_until_expire)
            return expiration_date.strftime("%Y-%m-%d")
        return "N/A"
