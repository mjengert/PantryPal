from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.lang import Builder

from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)
from kivymd.app import MDApp

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDList, MDListItemTrailingCheckbox
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.selectioncontrol import MDCheckbox

from item import Item
from groceryList import Grocery_List
from pantryList import Pantry_List

grocery_list = Grocery_List()
pantry_list = Pantry_List()

#################################### NAVIGATION BAR ####################################
class BaseMDNavigationItem(MDNavigationItem):
    # See https://kivymd.readthedocs.io/en/latest/components/navigation-bar/
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

############################### BASE SCREEN ####################################
class BaseScreen(MDScreen):
    image_size = StringProperty()
    #screen = MDScreen()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(
            FitImage(
                source=f"https://picsum.photos/{self.image_size}/{self.image_size}",
                size_hint=(0.9, 0.9),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                radius=dp(24),
            ),
        )

############################### GROCERY LIST SCREEN ####################################
class GroceryListScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        md_list = MDList(pos_hint={'center_y': 0.7})

        for i in range(grocery_list.getRange()):
            md_list_item = MDListItem(
                MDListItemHeadlineText(
                    text=grocery_list.getItem(i).getName()
                ),
                MDListItemTrailingCheckbox(),
               # on_release=self.on_tap_checkbox()
            )
            md_list.add_widget(md_list_item)

        self.add_widget(md_list)

    def on_tap_checkbox(self):
        print("tapped checkbox")


######################################### PANTRY PAL APP #####################################
class PantryPalUI(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text

    def on_checkbox_change(
            self,
            screen: GroceryListScreen,
            list: MDList,
            item: MDListItem,
            item_text: str,
            item_checkbox: MDListItemTrailingCheckbox
    ):
        self.root.get_ids().screen_manager.current = item_checkbox


    def build(self):
        return MDBoxLayout(
            MDScreenManager(
                BaseScreen(
                    name="Recipe Generator",
                    image_size="700"
                ),
                BaseScreen(
                    name="My Pantry",
                    image_size="600",
                ),
                BaseScreen(
                    name="Home",
                    image_size="1024",
                ),
                GroceryListScreen(
                    name="Grocery List",
                    #image_size="800",
                ),
                BaseScreen(
                    name="Coupons",
                    image_size="900"
                ),
                id="screen_manager",
            ),
            MDNavigationBar(
                BaseMDNavigationItem(
                    icon="pot-steam",
                    text="Recipe Generator",
                ),
                BaseMDNavigationItem(
                    icon="food-variant",
                    text="My Pantry",
                ),
                BaseMDNavigationItem(
                    icon="home",
                    text="Home",
                    active=True,
                ),
                BaseMDNavigationItem(
                    icon="format-list-bulleted",
                    text="Grocery List",
                ),
                BaseMDNavigationItem(
                    icon="tag",
                    text="Coupons"
                ),
                on_switch_tabs=self.on_switch_tabs,
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )


PantryPalUI().run()