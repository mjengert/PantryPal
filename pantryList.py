from item import Item
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.screen import MDScreen



class Pantry_List:
    def __init__(self):
        self.items = []
    
    def addToPantry(self,item):
        self.items.append(item)
    
    def removePantry(self,item):
        self.items.remove(item)
    
    def display(self):
        """Display all pantry items."""
        if not self.items:
            print("Your pantry is empty.")
            return
        for item in self.items:
            print(f"{item}")


class PantryScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pantry_list = Pantry_List()
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=50)


        self.p_scroll_view = ScrollView()
        self.p_list_layout = GridLayout(cols=2, padding=10, spacing=10)
        self.col_force_default = True  # Force default column width
        self.col_default_width = 50
        self.p_list_layout.bind(minimum_height=self.p_list_layout.setter('height'))

        self.p_scroll_view.add_widget(self.p_list_layout)

        self.layout.add_widget(Label(text="My Pantry", size_hint_y=None, height=60, color=(0.588,0.702,0.824,1),
                                     font_size=100, padding=40))
        self.layout.add_widget(self.p_scroll_view)

        self.add_widget(self.layout)

    def add_pantry_item(self, item):

        item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, size_hint_x=0.5)


        # Update the background rectangle's size and position when the item box changes

        label_box = BoxLayout(orientation='vertical')
        item_label = Label(text= item.getName(),color=(0,0,0,1),pos_hint={"center_x": 0.5}, font_size=40)
        exp_label = Label(text=item.getExpiration(), color=(0.5, 0.5, 0.5, 1), pos_hint={"center_x": 0.5},font_size=20)
        delete_button = Button(text="X", size_hint_x=None, width=40, background_color=(1, 0, 0, 1))
        delete_button.bind(on_press=lambda btn: self.delete_item(item, item_box))
        label_box.add_widget(item_label)
        label_box.add_widget(exp_label)
        item_box.add_widget(label_box)
        item_box.add_widget(delete_button)

        self.p_list_layout.add_widget(item_box)


    def delete_item(self, item, item_box):
        """Removes item from pantry list"""
        self.pantry_list.removePantry(item)
        self.p_list_layout.remove_widget(item_box)