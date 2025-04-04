from item import Item
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.screen import MDScreen
from pantryList import Pantry_List
class Grocery_List:
    def __init__(self):
        self.items = []

    def addToGrocery(self,item):
        self.items.append(item)
    
    def removeGrocery(self,item):
        self.items.remove(item)
    
    def checkOff(self,item, pantryList):
        self.items.remove(item)
        pantryList.addToPantry(item)

class GroceryScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grocery_list = Grocery_List()

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=50)
        self.text_input = TextInput(hint_text='Enter item name', multiline=False,size_hint = (0.5,None),pos_hint={"center_x": 0.5}, height = 50)
        self.text_input.bind(on_text_validate=self.create_item)

        self.g_scroll_view = ScrollView()
        self.g_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.g_list_layout.bind(minimum_height=self.g_list_layout.setter('height'))

        self.g_scroll_view.add_widget(self.g_list_layout)


        self.layout.add_widget(Label(text="Your Grocery List", size_hint_y=None, height=60, color=(0.588,0.702,0.824,1),
                                     font_size=100, padding=40))
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.g_scroll_view)


        self.add_widget(self.layout)

    def create_item(self, instance):
        item_name = self.text_input.text.strip()
        if item_name:
            new_item = Item(item_name)
            self.grocery_list.addToGrocery(new_item)

            item_box = BoxLayout(orientation='horizontal', size_hint = (0.5,None),pos_hint={"center_x": 0.5}, height=40)
            check_button = Button(text="Done", size_hint_x=None, width=80, background_color=(0, 1, 0, 1))
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = Label(text=new_item.getName(), color = (0,0,0,1))

            delete_button = Button(text="X", size_hint_x=None, width=40, background_color=(1, 0, 0, 1))
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''

    def check_off_item(self, item, item_box):
        """Moves item from grocery list to pantry list and calculates expiration date"""
        item.calcExpiration()
        self.grocery_list.checkOff(item, self.manager.get_screen("My Pantry").pantry_list)
        self.g_list_layout.remove_widget(item_box)

        pantry_screen = self.manager.get_screen("My Pantry")
        pantry_screen.add_pantry_item(item)

    def delete_item(self, item, item_box):
        """Removes item from grocery list"""
        self.grocery_list.removeGrocery(item)
        self.g_list_layout.remove_widget(item_box)
