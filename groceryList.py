from item import Item
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView


class Grocery_List:
    def __init__(self):
        self.items = {}

    def addToGrocery(self, item):
        if item not in self.items:
            self.items[item.getName()] = item

    def removeGrocery(self, item):
        del self.items[item.getName()]

    def checkOff(self, item, pantryList):
        self.removeGrocery(item)
        if item.getName() not in pantryList.items.keys():
            item.calcExpiration()
            pantryList.addToPantry(item)
            return True
        else:
            return False


class GroceryScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grocery_list = Grocery_List()

        self.layout = MDBoxLayout(orientation='vertical', _md_bg_color=(0.588, 0.702, 0.824, 0.25))
        self.text_input = MDTextField(multiline=False, size_hint=(0.6, 0.1),_md_bg_color=(0.588, 0.702, 0.824, 0.75),
                                    pos_hint={"center_x": 0.5},radius=[30, 30, 30, 30],halign="center")
        self.text_input.add_widget(MDTextFieldHintText(text='Enter a grocery item'))

        self.text_input.bind(on_text_validate=self.create_item)
        quick_selects = ['milk', 'eggs', 'bread', 'cereal', 'toilet paper', 'paper towels']
        self.quick_selects =MDGridLayout(cols=3,size_hint=(0.6, 0.25),
                                         pos_hint={"center_x": 0.5},padding=10,spacing=10)
        for item in quick_selects:
            quick_s_button = MDButton(theme_width="Custom",style='outlined',height="56dp", size_hint_x=.5)
            quick_s_button.add_widget(MDButtonText(text=item))
            quick_s_button.bind(on_press=lambda btn, qItem=item: self.create_item_quick(qItem))
            self.quick_selects.add_widget(quick_s_button)

        self.g_scroll_view = MDScrollView(size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5})
        self.g_list_layout = MDGridLayout(cols=2, spacing=10)
        self.g_list_layout.bind(minimum_height=self.g_list_layout.setter('height'))

        self.g_scroll_view.add_widget(self.g_list_layout)

        self.title = MDLabel(text="Your Grocery List", pos_hint={"center_x": 0.5},padding='5sp', halign='center',size_hint=(1, 0.15),
                                       text_color=(0.588, 0.702, 0.824, 1),_md_bg_color=(0.588, 0.702, 0.824, .1))
        self.title.font_size= '50sp'
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.quick_selects)
        self.layout.add_widget(self.g_scroll_view)

        self.add_widget(self.layout)

    def create_item(self, instance):
        item_name = self.text_input.text.strip()
        if item_name and item_name not in self.grocery_list.items.keys():
            new_item = Item(item_name)
            self.grocery_list.addToGrocery(new_item)

            # create box to hold grocery item
            item_box = MDBoxLayout(orientation='horizontal', size_hint=(None, None),height=75,
                                   width=self.g_list_layout.width * 0.5,radius=[25,25,25,25],
                                   _md_bg_color=(0.588, 0.702, 0.824, .5))
            check_button = MDIconButton(icon='check',valign='center')
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = MDLabel(text=new_item.getName(), text_color=(0, 0, 0, 1), pos_hint={"center_x": 0.5},
                            halign='center')

            delete_button = MDIconButton(icon='trash-can-outline', valign='center')
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            # add widgets to layout
            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''

    def create_item_quick(self, item_name):
        if item_name and item_name not in self.grocery_list.items.keys():
            new_item = Item(item_name)
            self.grocery_list.addToGrocery(new_item)

            # create box to hold grocery item
            item_box = MDBoxLayout(orientation='horizontal', pos_hint={"center_y": 0.5},size_hint=(None, None),height=75,
                                   width=self.g_list_layout.width * 0.5,radius=[25,25,25,25],
                                   _md_bg_color=(0.588, 0.702, 0.824, .5))
            check_button = MDIconButton(icon='check', valign='center',pos_hint={"center_y": 0.5})
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = MDLabel(text=new_item.getName(), color=(0, 0, 0, 1),pos_hint={"center_x": 0.5},
                            halign='center')

            delete_button = MDIconButton(icon='trash-can-outline', valign='center', pos_hint={"center_y": 0.5})
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            # add widgets to layout
            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''

    def check_off_item(self, item, item_box):
        """Moves item from grocery list to pantry list and calculates expiration date"""

        pantry_screen = self.manager.get_screen("My Pantry")
        pantry_list = pantry_screen.pantry_list
        if self.grocery_list.checkOff(item, pantry_list):
            self.g_list_layout.remove_widget(item_box)
            pantry_screen.add_pantry_item(item)
        else:
            self.g_list_layout.remove_widget(item_box)
            pantry_screen.update_item(item)

    def delete_item(self, item, item_box):
        """Removes item from grocery list"""
        self.grocery_list.removeGrocery(item)
        self.g_list_layout.remove_widget(item_box)
