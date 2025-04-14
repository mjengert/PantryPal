import time

from bs4 import BeautifulSoup
from scrapfly import ScrapflyClient, ScrapeConfig
from parsel import Selector
import logging

class PriceScraper:

    # initialize the PriceScraper class with the Scrapfly API key
    def __init__(self, apiKey):
        logging.getLogger("scrapfly").setLevel(logging.DEBUG)
        self.client = ScrapflyClient(apiKey)
        self.retrievedProductData = {}

    # returns the price of the product at the given URL
    def getProductData(self, url, retries=5):
        # determine which website the URL is from
        if "publix" in url:
            store = "Publix"
            wait_for_selector = "div[class*='price'] span"
        elif "walmart" in url:
            store = "Walmart"
            wait_for_selector = "div[data-testid='price']"
        # if the number of retries is exceeded, return None
        if retries == 0:
            print("Failed to retrieve price")
            return [store, "None", "None"]
        # scrape the URL and wait for the price element to load
        apiResult = self.client.scrape(ScrapeConfig(
            url=url,
            render_js=True,
            proxy_pool="public_datacenter_pool",
            wait_for_selector=wait_for_selector
        ))
        # parse the HTML content of the API result and extract the price and product name
        soup = BeautifulSoup(apiResult.content, 'html.parser')
        selector = Selector(text=apiResult.content)
        if store == "Publix":
            price = selector.xpath('//*[@id="item_details"]/div[2]/div[2]/div[2]/div/div/div[1]/div/div/span[1]/span/text()').get()
            produceName = selector.xpath('//*[@id="item_details"]/div[2]/div[2]/div[1]/h1/span/text()').get()
        else:
            price = selector.xpath('//*[@id="maincontent"]/section/main/div[2]/div[2]/div/div[3]/div/div[1]/div/div/span[1]/span[2]/span/text()').get()
            produceName = selector.xpath('//*[@id="main-title"]/text()').get()

        # if price is found, return it
        if price and produceName:
            product = [store, (produceName or "Not Found").strip(), (price or "Not Found").strip()]
            return product
        # if price is not found, retry function
        else:
            print(f"Retrying {url}... ({retries} attempts left)")
            return self.getProductData(url, retries - 1)

    def startScraping(self):
        # get the user's zip code to display prices for the user's location
        get = input("Enter your zip code: ")
        userZipCode = get
        # define the products to display prices for (only a few examples for the prototype)
        displayProducts = [
            "https://delivery.publix.com/store/publix/products/2691738-sargento-reduced-fat-low-moisture-part-skim-mozzarella-natural-cheese-light-string-cheese-snacks-9-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/33223295-kellogg-froot-loops-breakfast-cereal-kids-cereal-family-breakfast-original-17-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/23587546-doritos-nacho-tortilla-chips-14-5-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/16408559-fairlife-2-reduced-fat-ultrafiltered-milk-lactose-free-52-fl-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/103945-nature-s-own-butterbread-bread-20-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/2691844-bush-s-best-brown-sugar-hickory-baked-beans-28-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/144054-barilla-classic-blue-box-pasta-rotini-1-lb?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/16408707-hidden-valley-ranch-salad-dressing-16-fl-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/16409607-minute-rice-white-rice-14-oz?zipcode={}".format(
                userZipCode),
            "https://delivery.publix.com/store/publix/products/73051-jif-peanut-butter-16-oz?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Fairlife-2-Reduced-Fat-Ultra-Filtered-Milk-52-fl-oz/43984343?classType=REGULAR&athbdg=L1200?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Kellogg-s-Froot-Loops-Original-Breakfast-Cereal-Family-Size-16-6-oz-Box/3729155340?classType=VARIANT?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Nature-8217-s-Own-Sliced-Butter-Bread-20-oz/10450012?classType=REGULAR&athbdg=L1200?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Sargento-Natural-String-Cheese-Snacks-12-Count/10291588?classType=REGULAR&athbdg=L1600&from=/search?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Doritos-Nacho-Cheese-Tortilla-Snack-Chips-Party-Size-14-5-oz-Bag/433078517?classType=REGULAR&athbdg=L1600?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Bush-s-Brown-Sugar-Hickory-Baked-Beans-Canned-Beans-28-oz-Can/45207653?classType=VARIANT&from=/search?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Barilla-Classic-Non-GMO-Kosher-Certified-Rotini-Pasta-16-oz/10309181?classType=VARIANT&athbdg=L1200&from=/search?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Hidden-Valley-Original-Ranch-Salad-Dressing-and-Topping-16-Ounce-Bottle/10451460?classType=VARIANT&athbdg=L1600&from=/search?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Minute-Instant-White-Rice-Light-and-Fluffy-Gluten-Free-14-oz/10848964?classType=VARIANT&athbdg=L1200&from=/search?zipcode={}".format(
                userZipCode),
            "https://www.walmart.com/ip/Jif-Creamy-Peanut-Butter-16-Ounce-Jar/777839120?classType=VARIANT&athbdg=L1200&from=/search?zipcode={}".format(
                userZipCode)
        ]
        # fetch and display prices for predefined products at Target
        print("Fetching prices...")
        for product in displayProducts:
            # call the getProductData method to retrieve product data
            productData = self.getProductData(product)
            if "$" in productData[2]:
                productData[2] = productData[2].replace("$", "")
            # store the product data in a dictionary
            # if the product dict is empty, add the product data to it
            if not self.retrievedProductData:
                self.retrievedProductData[productData[1]] = [productData[0], productData[2]]
            # if the product list isn't empty, check if the product is already in the list (will have the same first word)
            else:
                if "'" in productData[1]:
                    productFirstWord = productData[1].split("'")[0]
                else:
                    productFirstWord = productData[1].split(" ")[0]
                for existingProduct in list(self.retrievedProductData.keys()):
                    if "'" in existingProduct:
                        existingProductFirstWord = existingProduct.split("'")[0]
                    else:
                        existingProductFirstWord = product.split(" ")[0]
                    if productFirstWord == existingProductFirstWord:
                        # if the price is lower, update the price name and store
                        if float(productData[2]) < float(self.retrievedProductData[existingProduct][1]):
                            # remove the existing product from the list
                            del self.retrievedProductData[existingProduct]
                            # add the new product to the list
                            self.retrievedProductData[productData[1]] = [productData[0], productData[2]]
                        break
                    # if the product is not in the list, add it to the list
                    else:
                        self.retrievedProductData[productData[1]] = [productData[0], productData[2]]
            # print the retrieved product data
            time.sleep(10)
            print(f'{productData[1]} at {productData[0]} costs {productData[2]}')
