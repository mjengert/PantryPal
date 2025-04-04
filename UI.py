from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

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
from groceryList import GroceryScreen
from pantryList import PantryScreen



class BaseMDNavigationItem(MDNavigationItem):
    # See https://kivymd.readthedocs.io/en/latest/components/navigation-bar/
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))


class BaseScreen(MDScreen):
    image_size = StringProperty()

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


class Example(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.get_ids().screen_manager.current = item_text

    def build(self):
        return MDBoxLayout(
            MDScreenManager(
                BaseScreen(
                    name="Recipe Generator",
                    image_size="700"
                ),
                PantryScreen(
                    name="My Pantry",
                ),
                BaseScreen(
                    name="Home",
                    image_size="1024",
                ),
                GroceryScreen(
                    name="Grocery List",
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


Example().run()