import os
from dotenv import load_dotenv
from priceScraper import PriceScraper

# load the Scrapfly API key from the .env file
load_dotenv()
apiKey = os.getenv("SCRAPFLY_API_KEY")

# create an instance of the PriceScraper class and start scraping prices
priceScraper = PriceScraper(apiKey)
priceScraper.startScraping()




