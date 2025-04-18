from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
import os
from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup
from kivy.properties import StringProperty
import time
import re
SCRAPFLY_API_KEY = "scp-test-9c8f6362dd6c4560ab47d820f11a2c03"
scrapfly = ScrapflyClient(key=SCRAPFLY_API_KEY)
class Coupon:
    def __init__(self,title,price,promo):
        self.title=title
        self.price=price
        self.promo=promo

    def getTitle(self):
        return self.title

    def getPrice(self):
        return self.price

    def getPromo(self):
        return self.promo


def scrape_target(max_retries=3, wait_between_retries=5):
    url = "https://www.target.com/c/grocery-deals/-/N-k4uyq?type=products"

    scrape_config = ScrapeConfig(
        url=url,
        render_js=True,
        auto_scroll=True,
        rendering_wait=5000,
        wait_for_selector='[data-test*="ProductCardWrapper"]',
    )

    target_deals = []
    # Loop to retry scraping if no product cards are found
    for attempt in range(1, max_retries + 1):
        result = scrapfly.scrape(scrape_config)
        html_content = result.content

        soup = BeautifulSoup(html_content, "html.parser")
        product_cards = soup.select('[data-test*="ProductCardWrapper"]')

        if len(product_cards) > 0:
            for card in product_cards:
                title_el = card.select_one('[data-test*="product-title"]')
                price_el = card.select_one('[data-test*="current-price"]')
                promo_el = card.select_one('[data-test="first-regular-promo"]')

                # Skip placeholder cards with no title
                if title_el is None or not title_el.get_text(strip=True):
                    continue

                title = title_el.get_text(strip=True)
                price = price_el.get_text(strip=True) if price_el else None
                promo_message = promo_el.get_text(strip=True) if promo_el else None

                # If there's no promo, we skip this card
                if not promo_message:
                    continue

                target_deals.append(Coupon(title,price,promo_message))

            break
        else:
            if attempt < max_retries:
                time.sleep(wait_between_retries)

    return target_deals


def scrape_walmart():
    url = "https://www.walmart.com/shop/walmart-member-item-rewards/grocery?facet=reward_eligible%3AWalmart+Cash+eligible"
    scrape_config = ScrapeConfig(
        url=url,
        render_js=True,
        auto_scroll=True,
        rendering_wait=5000,
        wait_for_selector='[data-item-id]'
    )

    with ScrapflyClient(key=SCRAPFLY_API_KEY) as client:
        result = client.scrape(scrape_config)
    html_content = result.content

    soup = BeautifulSoup(html_content, "html.parser")

    # Select all product cards
    product_cards = soup.select('[data-item-id]')

    walmart_deals = []

    for card in product_cards:
        # Extract the product title
        title_el = card.select_one('a span.w_iUH7')
        if not title_el:
            continue
        title_text = title_el.get_text(strip=True)

        # Extract the current/promotional price
        current_price_el = None
        for span in card.select('span'):
            span_text = span.get_text(strip=True)
            if "current price" in span_text.lower():
                current_price_el = span
                break

        if current_price_el:
            current_price_text = current_price_el.get_text(strip=True)
            # Remove literal phrase "current price"
            current_price_text = re.sub(r'(?i)current price\s*', '', current_price_text).strip()
            # If also wanting to remove "Now" and only show the price, uncomment:
            current_price_text = re.sub(r'(?i)now\s*', '', current_price_text).strip()
        else:
            current_price_text = None

        # Extract the "Was" price if any
        was_price_el = None
        for span in card.select('span'):
            span_text = span.get_text(strip=True)
            if "was" in span_text.lower():
                was_price_el = span
                break
        was_price_text = was_price_el.get_text(strip=True) if was_price_el else None

        # If  also waning to remove "Was", uncomment the next line:
        was_price_text = re.sub(r'(?i)was\s*', '', was_price_text).strip() if was_price_text else None

        if not was_price_text:
            # Skip if theres no 'was' price
            continue

        # Build the final product dict
        promo_message=f"{title_text} is discounted from {was_price_text} to {current_price_text}"
        walmart_deals.append(Coupon(title_text,current_price_text,promo_message))

    return walmart_deals
"""if __name__ == "__main__":
    try:
        deals = scrape_target_grocery_deals()
        if not deals:
            print("No deals were scraped. Please try again later.")
            exit()

        search_query = input("Enter item name to search for coupons: ").lower().strip()

        matching_deals = [deal for deal in deals if deal["title"] and search_query in deal["title"].lower()]

        if matching_deals:
            print(f"\nCoupons for '{search_query}':")
            for idx, item in enumerate(matching_deals, start=1):
                print(f"{idx}. Title: {item['title']!r} | Price: {item['price']!r} | Promo: {item['promo']!r}")
        else:
            print(f"\nNo coupons found for '{search_query}'.")
    except Exception as e:
        print(f"Error during scraping: {e}")"""

class CouponScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coupons={
            'Target': scrape_target(),
            'Walmart': scrape_walmart()
        }
        self.light_primary = self.theme_cls.primaryColor[:3] + [.1]
        self.layout = MDBoxLayout(orientation='vertical')
        self.text_input = MDTextField(multiline=False, size_hint=(0.6, 0.1),pos_hint={"center_x": 0.5},
                                      radius=[30, 30, 30, 30],halign="center")
        self.text_input.add_widget(MDTextFieldHintText(text='Enter the name of an Item'))
        self.store_buttons = MDGridLayout(cols=2,size_hint=(0.6, 0.1),
                                         pos_hint={"center_x": 0.5},padding=10,spacing=10)


        self.c_scroll_view = MDScrollView(size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5})
        self.c_list_layout = MDGridLayout(cols=1, spacing=10,pos_hint={"center_x": 0.5}, padding=10,size_hint_y=None)
        self.c_list_layout.bind(minimum_height=self.c_list_layout.setter('height'))

        self.c_scroll_view.add_widget(self.c_list_layout)

        self.title = MDLabel(text="Shopping Around", pos_hint={"center_x": 0.5},padding='5sp', halign='center',size_hint=(1, 0.15),
                             text_color=self.theme_cls.primaryColor)
        self.title.font_size= '50sp'
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.store_buttons)
        self.layout.add_widget(self.c_scroll_view)

        self.add_widget(self.layout)

    def filter_coupons(self, store):
        self.selected_store = store
        container = self.c_list_layout
        container.clear_widgets()
        if self.coupons.get(store):
            for coupon in self.coupons.get(store):
                if coupon:
                    item_box = MDBoxLayout(orientation='horizontal', size_hint=(0.5, None), height=125,
                                          radius=[25, 25, 25, 25],pos_hint={"center_x": 0.5},
                                           _md_bg_color=self.light_primary)


                    label = MDLabel(text=coupon.getPromo(), text_color=self.theme_cls.primaryColor[:3]+[.9], pos_hint={"center_x": 0.5},
                                    halign='center')
                    item_box.add_widget(label)
                    self.c_list_layout.add_widget(item_box)
        else:
            item_box = MDBoxLayout(orientation='horizontal', size_hint=(0.5, None), height=125,
                                radius=[25, 25, 25, 25],pos_hint={"center_x": 0.5},
                                   _md_bg_color=self.light_primary)

            label = MDLabel(text='No Coupons  Found', text_color=self.theme_cls.primaryColor[:3]+[.9], pos_hint={"center_x": 0.5},
                            halign='center')
            item_box.add_widget(label)
            self.c_list_layout.add_widget(item_box)



