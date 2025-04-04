from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDList, MDListItemTrailingCheckbox
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.selectioncontrol import MDCheckbox

from item import Item
from groceryList import Grocery_List
from pantryList import Pantry_List
class PantryPal(MDApp):


    def create_item(self, instance):
        item_name = self.text_input.text.strip()
        if item_name:
            new_item = Item(item_name)
            self.grocery_list.addToGrocery(new_item)

            item_box = BoxLayout(orientation = 'horizontal', size_hint_y = None, height =40)
            check_button = Button(text="Done", size_hint_x=None, width=80, background_color = (0, 1, 0, 1))
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = Label(text=new_item.getName())

            delete_button = Button(text="X", size_hint_x=None, width=40,  background_color = (1, 0, 0, 1))
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''  # Clear input field

    def check_off_item(self, item, item_box):
        """Moves item from grocery list to pantry list and calculates expiration date"""
        item.calcExpiration()
        self.grocery_list.checkOff(item, self.pantry_list)
        self.g_list_layout.remove_widget(item_box)

        pantry_item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        pantry_label = Label(text=f"{item.getName()} expires on {item.getExpiration()}")
        pantry_item_box.add_widget(pantry_label)

        self.p_list_layout.add_widget(pantry_item_box)

    def delete_item(self, item, item_box):
        """Removes item from grocery list"""
        self.grocery_list.removeGrocery(item)
        self.g_list_layout.remove_widget(item_box)

    def build(self):
        self.grocery_list = Grocery_List()
        self.pantry_list = Pantry_List()
        screen = MDScreen(md_bg_color=self.theme_cls.backgroundColor)
        md_list = MDList(pos_hint={'center_y':0.7})

        #first_item = self.grocery_list.getItem(0)

        #self.md_list_items = []
        for i in range(self.grocery_list.getRange()):
            md_list_item = MDListItem(
                #MDCheckbox(halign='left', pos_hint={'center_x':0.5, 'center_y':0.5}),
                MDListItemHeadlineText(
                    text=self.grocery_list.getItem(i)
                ),
                MDListItemTrailingCheckbox()
            )
            md_list.add_widget(md_list_item)

        screen.add_widget(md_list)
        return screen

        '''
        self.layout = BoxLayout(orientation = 'horizontal', spacing = 10, padding = 10 )

        self.grocery_sect = BoxLayout(orientation='vertical',size_hint = (0.5,1))
        self.text_input = TextInput(hint_text='Enter item name', multiline=False)
        self.text_input.bind(on_text_validate=self.create_item)

        self.g_scroll_view = ScrollView()
        self.g_list_layout = GridLayout(cols=1, size_hint_y=None)
        self.g_list_layout.bind(minimum_height=self.g_list_layout.setter('height'))

        self.g_scroll_view.add_widget(self.g_list_layout)

        self.grocery_sect.add_widget(self.text_input)
        self.grocery_sect.add_widget(self.g_scroll_view)

        self.pantry_sect = BoxLayout(orientation='vertical',size_hint = (0.5,1))

        self.p_scroll_view = ScrollView()
        self.p_list_layout = GridLayout(cols=1, size_hint_y=None)
        self.p_list_layout.bind(minimum_height=self.g_list_layout.setter('height'))

        self.p_scroll_view.add_widget(self.p_list_layout)

        self.pantry_sect.add_widget(Label(text = "Pantry List", size_hint_y = None, height = 40))
        self.pantry_sect.add_widget(self.p_scroll_view)

        self.layout.add_widget(self.grocery_sect)
        self.layout.add_widget(self.pantry_sect)
        

        return self.layout
        '''


if __name__ == '__main__':
    PantryPal().run()
