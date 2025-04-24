# PantryPal
# Project Description
PantryPal is a cross-platform mobile app developed with KivyMD and MongoDB, designed to help users organize their food inventory, reduce waste, and save money. This app helps users keep track of what they already have at home, discover new recipes, and scrape real-time deals from stores like Target and Walmart. Combining intuitive design with useful automation, PantryPal is an ideal solution for students, families, and meal preppers looking to simplify shopping, cooking, and budgeting.
# Challenge and Solution
Grocery shopping, once a straightforward task, has become increasingly complicated with the emergence of new-age stores that all sell similar products at various prices. This makes it difficult for customers to find the best deals and the cheapest options closest to them. As a result, competitive price strategies affect consumers by limiting their purchasing power and can create a stressful experience for shoppers.

To solve this increasing social issue, our team sought to design an application to make grocery shopping a stress-free experience. The app provides users with easy-to-access price comparisons from nearby grocery stores. Further, the app encompasses grocery list management, recipe recommendations, and current coupon information. Other features include populated expiration dates to help users track when their groceries will expire and a user-friendly interface to tie it all together.
# Features and Functionality
# Recipe Generation
This feature offers several key functions of the PantryPal application. After adding a grocery item to the user's Pantry List, recipes will be populated on the corresponding Recipe Screen. Each recipe card displays an image of the finished recipe, the name, and the user's missing and owned ingredients. Additionally, when a recipe is clicked or tapped on by the user, more information related to the recipe will be displayed. The prototype recipe information screen only includes an image, summary, and ingredient list. However, this can easily be expanded upon in the future. The last functionality of this screen involves a plus sign button displayed on each recipe card. When the user uses this button, the ingredients that the user is missing for the recipe will instantly be added to their grocery list, and a popup message will appear indicating this function.
# Grocery List
This feature also offers several of the key features of the PantryPal application. Using the grocery list the user can add, remove and check off items to track the items that they need to shop for.The grocery list allows users to add items in  two different ways the first is using a search bar in which the user can type and item and add it to the list the second being a predetermined set of buttons with common grocery items. The grocery list page will then display each item in a separate item box including a check off and delete button. If the delete button is clicked the item will be removed from the page as well as from the users internal grocery list. If the check off is clicked the item will be moved from the grocery list to the users pantry list and removed from the page. 
# Pantry List
This feature works alongside the grocery list and recipe generator to round out our user experience. The pantry list tracks the items that the user currently has in their home. Upon transfer from the grocery list to the pantry list the items expiration date is estimated. The item is displayed in the pantry list with the item name, expiration date, and a remove button. Upon clicking the remove button the item is deleted from the pantry page and the users internal pantry list. This internal pantry list is then used in the recipe generator to generate recipes.
# Coupon and Price Scraper
This feature is a standout feature in our application. This feature collects coupons from different stores currently walmart and target and displays them on the coupons screen. Using the two buttons with store names you can view the coupons from each store individually. This page also includes a search bar that can be used to filter the coupons based on a text input. The text box will also allow the user to compare store prices for a variety of stores for particular items. While this feature is not currently fully implemented with the user interface it is implemented on the backend.

# Technical Details
Technical Description
Technical Details
Languages: Python
Libraries: KivyMD
APIs: Spoonacular, Scrapfly, MongoDB
Development tools: PyCharm

Installation Instructions
Kivy 2.3.1
Kivy-Garden 0.1.5
Pygments 2.19.1
annotated-types 0.7.0
asyncgui 0.6.3
asynckivy 0.6.4
backoff 2.2.1
beautifulsoup4 4.13.4
certifi 2025.1.31
charset-normalizer 3.4.1
cssselect 1.3.0
decorator 5.2.1
dnspython 2.7.0
docutils 0.21.2
filetype 1.2.0
idna 3.10
jmespath 1.0.1
kivymd 2.0.1.dev0
kivymd2 2.0.1
loguru 0.7.3
lxml 5.3.2
materialyoucolor 2.0.10
packaging 24.2
parsel 1.10.0
pillow 11.2.1
pip 25.0.1
pydantic 2.11.3
pydantic_core 2.33.1
pymongo 4.12.0
python-dateutil 2.9.0.post0
python-dotenv 1.1.0
requests 2.32.3
scrapfly-sdk 0.8.21
six 1.17.0
soupsieve 2.7
spoonacular 3.0
typing-inspection 0.4.0
typing_extensions 4.13.2
urllib3 2.4.0
w3lib 2.3.1

# User Login Information
Username: sample
Password: password
