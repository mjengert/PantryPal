from bs4 import BeautifulSoup
from scrapfly import ScrapflyClient, ScrapeConfig
from parsel import Selector
import logging

class PriceScraper:

    # initialize the PriceScraper class with the Scrapfly API key
    def __init__(self, apiKey):
        logging.getLogger("scrapfly").setLevel(logging.DEBUG)
        self.client = ScrapflyClient(apiKey)

    # returns the price of the product at the given URL
    def getPrice(self, url, retries=5):
        # if the number of retries is exceeded, return None
        if retries == 0:
            print("Failed to retrieve price")
            return None
        # scrape the URL and wait for the price element to load
        apiResult = self.client.scrape(ScrapeConfig(
            url=url,
            render_js=True,
            wait_for_selector="span[data-test='product-price']",
        ))

        # parse the HTML content of the API result and extract the price and product name
        soup = BeautifulSoup(apiResult.content, 'html.parser')
        selector = Selector(text=apiResult.content)
        price = selector.xpath("//span[@data-test='product-price']/text()").get()
        product = selector.xpath("//h1/text()").get()

        # if the price is not found, try to extract it from the page using a different selector
        if not price:
            price = selector.css("span[data-test='product-price']::text").get()
        # if price is found, return it
        if price:
            return price.strip()
        # if price is not found, retry function
        else:
            return self.getPrice(url, retries - 1)

    def startScraping(self):
        # get the user's zip code to display prices for the user's location
        get = input("Enter your zip code: ")
        userZipCode = get
        # define the products to display prices for (only a few examples for the prototype)
        displayProductsTarget = {
            "https://www.target.com/p/vital-farms-pasture-raised-grade-a-large-eggs-12ct/-/A-18783617?zipcode={}".format(
                userZipCode),
            "https://www.target.com/p/kellogg-s-froot-loops-breakfast-cereal/-/A-89089421?preselect=89529587?zipcode={}".format(
                userZipCode),
            "https://www.target.com/p/nature-39-s-own-butter-bread-20oz/-/A-13151711?zipcode={}".format(
                userZipCode),
            "https://www.target.com/p/fairlife-lactose-free-skim-milk-52-fl-oz/-/A-17093210?zipcode={}".format(
                userZipCode),
            "https://www.target.com/p/doritos-nacho-cheese-chips-9-25oz/-/A-14930889?zipcode={}".format(
                userZipCode)
        }
        # to be implemented in the future
        displayProductsAldi = {

        }
        # fetch and display prices for predefined products at Target
        print("Fetching prices...")
        for product in displayProductsTarget:
            price = self.getPrice(product)
            self.retrievedPrices["Target"] = [product, price]
            print(f"Price at Target: {price}")






