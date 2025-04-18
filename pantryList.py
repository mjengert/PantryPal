from item import Item
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.color_definitions import colors



class Pantry_List:
    def __init__(self):
        self.items = {}

    def addToPantry(self, item):
        self.items[item.getName()] = item

    def removePantry(self, item):
        del self.items[item.getName()]

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
        self.item_widgets = {}
        self.layout = MDBoxLayout(orientation='vertical')
        self.light_primary = self.theme_cls.primaryColor[:3] + [.1]

        self.p_scroll_view = MDScrollView(size_hint=(0.8, 0.89), pos_hint={"center_x": 0.5})
        self.p_list_layout = MDGridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        self.p_list_layout.bind(minimum_height=self.p_list_layout.setter('height'))

        self.p_scroll_view.add_widget(self.p_list_layout)

        self.title = MDLabel(text="My Pantry", pos_hint={"center_x": 0.5}, padding='5sp', halign='center',
                             size_hint=(1, 0.11), theme_text_color="Custom", text_color=self.theme_cls.primaryColor)
        self.title.font_size = '50sp'
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.p_scroll_view)

        self.add_widget(self.layout)
        for item in self.pantry_list:
            self.add_pantry_item(item)
    def add_pantry_item(self, item):
        # create box to hold pantry item
        item_box = MDBoxLayout(orientation='horizontal', size_hint=(None, None), height=100,
                               width=self.p_list_layout.width * 0.49, radius=[25, 25, 25, 25],
                               _md_bg_color=self.light_primary)

        # box to vertically stack labels
        label_box = MDBoxLayout(orientation='vertical', size_hint=(1, .9))
        item_label = MDLabel(text=item.getName(), text_color=self.theme_cls.primaryColor[:3] + [.9], halign='center')
        item_label.font_size = '24sp'
        exp_label = MDLabel(text=item.getExpiration(), text_color=self.theme_cls.primaryColor[:3] + [.5],
                            halign='center')
        exp_label.font_size = '10sp'

        delete_button = MDIconButton(icon='trash-can-outline', valign='center')
        delete_button.bind(on_press=lambda btn: self.delete_item(item))

        # add widgets to layout
        label_box.add_widget(item_label)
        label_box.add_widget(exp_label)
        item_box.add_widget(label_box)
        item_box.add_widget(delete_button)

        self.p_list_layout.add_widget(item_box)
        self.item_widgets[item.getName()] = item_box

    def delete_item(self, item):
        if item.getName() in self.item_widgets:
            item_box = self.item_widgets[item.getName()]
            self.p_list_layout.remove_widget(item_box)
            self.pantry_list.removePantry(item)
            del self.item_widgets[item.getName()]

    def update_item(self, item):
        self.delete_item(item)
        item.calcExpiration()
        self.pantry_list.addToPantry(item)
        self.add_pantry_item(item)

    def set_new_exp(self, item):
        pass
