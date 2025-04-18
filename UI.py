from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarLeadingButtonContainer, MDActionTopAppBarButton, MDTopAppBarTitle
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText, MDIconButton
from kivymd.uix.card import MDCard

from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
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

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDList, MDListItemTrailingCheckbox, \
    MDListItemSupportingText, MDListItemTrailingIcon, MDListItemLeadingAvatar, MDListItemTertiaryText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from item import Item
from groceryList import Grocery_List
from pantryList import Pantry_List
from recipeGenerator import RecipeGenerator
from UserData import *

#****************** Pulling Data from Database *********************#
user = UserData("sample")

grocery_list = user.getGroceryList()
pantry_list = user.getPantryList()

#################################### NAVIGATION BAR ####################################
class BaseMDNavigationItem(MDNavigationItem):
    # See https://kivymd.readthedocs.io/en/latest/components/navigation-bar/
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))

class CustomCheckbox(MDListItem):
    pressed = ListProperty([0,0])


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

################################ RECIPE GENERATOR SCREEN ####################################

class RecipeGenScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addedMissing = False

        # creates a layout for the list to be added to
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            padding=dp(10),
        )
        self.add_widget(layout)

        # creates search bar
        searchBar = MDTextField(
            MDTextFieldHintText(text="Search for recipe"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "center_y": 0.9},
        )
        layout.add_widget(searchBar)

        # adds scroll functionality to the screen
        scroll = MDScrollView()
        layout.add_widget(scroll)

        # creates a list to hold the recipes and add it to the scroll view
        md_list = MDList(
            pos_hint={'center_y': 0.7},
            size_hint=(1, None),
            height=dp(400),
        )
        scroll.add_widget(md_list)

        # calling the recipe generator API
        recipeGen = RecipeGenerator()

        # get the ingredients from the pantry
        ingredients = []
        for i in range(pantry_list.getRange()):
            ingredients.append(pantry_list.getItem(i).getName())

        # get the recipes based on the ingredients
        recipeGen.generateRecipe(ingredients)

        # get recipe info from the API
        for recipe in recipeGen.recipeList:
            recipeGen.getRecipeInfo(recipe)

        # if pantry list is empty, show default recipes
        if recipeGen.recipeList == []:
            md_list.add_widget(MDListItem(text='No recipes found'))

        # if pantry list is not empty, show recipes based on pantry items
        else:
            for recipe in recipeGen.recipeList:
                # creates a list item for each recipe
                # display the recipe name
                md_list_item = MDListItem(
                    # display the recipe name
                    MDListItemHeadlineText(
                        text=recipe.getName()
                    ),
                    # display the recipe image
                    MDListItemLeadingAvatar(
                        source=recipe.getImage()
                    ),
                    # display the recipe ingredients owned
                    MDListItemSupportingText(
                        text="Owned Ingredients: " + recipe.ownedIngredients()
                    ),
                    # display the recipe ingredients missing
                    MDListItemTertiaryText(
                        text="Missing Ingredients: " + recipe.missingIngredients()
                    ),
                )

                # adds button to automatically add missing ingredients to grocery list
                addMissingButton = MDIconButton(
                    icon="plus",
                    style="filled",
                    md_bg_color=self.theme_cls.secondaryColor,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                # binds the buttons to their functions
                addMissingButton.bind(on_release=lambda instance, r=recipe: self.missingIngredients(instance, r))
                md_list_item.add_widget(addMissingButton)
                md_list_item.bind(on_release=lambda instance, r=recipe: self.recipeInfo(r))
                md_list.add_widget(md_list_item)

    # function to display the recipe information when the recipe is clicked
    def recipeInfo(self, recipe):
        # check if recipe screen already exists
        if self.manager.has_screen("Recipe Info"):
            self.manager.remove_widget(self.manager.get_screen("Recipe Info"))

        # creates a new screen to display the recipe information
        recipeInfoScreen = RecipeInfoScreen(name="Recipe Info", recipe=recipe)
        self.manager.add_widget(recipeInfoScreen)
        self.manager.transition.direction = "left"
        self.manager.current = "Recipe Info"

    # function to add or remove missing ingredients from grocery list
    def missingIngredients(self, instance, recipe):
        # check if the ingredients were already added to the grocery list; if so, remove them
        if self.addedMissing:
            self.deleteMissingIngredients(instance, recipe)

        # otherwise, add them to the grocery list
        else:
            self.addMissingIngredients(instance, recipe)

    # function to add missing ingredients to grocery list, toggle icon, and announcement
    def addMissingIngredients(self, instance, recipe):
        self.toggleIcon(instance)
        self.toggleAnnouncment("Missing ingredients added to grocery list")
        self.addedMissing = True

    # function to remove missing ingredients from grocery list, toggle icon, and announcement
    def deleteMissingIngredients(self, instance, recipe):
        self.toggleIcon(instance)
        self.toggleAnnouncment("Missing ingredients removed from grocery list")
        self.addedMissing = False

    # function to toggle the icon of the button when pressed
    def toggleIcon(self, instance):
        if instance.icon == "plus":
            instance.icon = "check"
        else:
            instance.icon = "plus"

    # function to toggle the announcement message when button is pressed
    def toggleAnnouncment(self, announcement):
        # remove the previous announcement if it exists
        if hasattr(self, announcement):
            self.remove_widget(announcement)

        # creates announcement message layout
        self.layout = MDBoxLayout(
            orientation="vertical",
            size_hint=(0.3, None),
            height=dp(50),
            padding=dp(10),
            md_bg_color=self.theme_cls.primaryColor,
            pos_hint={"center_x": 0.5, "top": 0.95},
        )

        # creates the announcement message label
        self.announcement = MDLabel(
            text=announcement,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )

        # adds the announcement message to the layout and sets timer to remove it
        self.layout.add_widget(self.announcement)
        self.add_widget(self.layout)
        Clock.schedule_once(lambda dt: self.removeAnnouncement(), 3)

    # function to remove the announcement message after 3 seconds
    def removeAnnouncement(self):
        # if the announcement exists, remove it and its layout
        if hasattr(self, "layout"):
            self.remove_widget(self.layout)
            self.layout = None
        if hasattr(self, "announcement"):
            self.remove_widget(self.announcement)
            self.announcement = None


############################### RECIPE INFO SCREEN ####################################
class RecipeInfoScreen(MDScreen):

    def __init__(self, recipe, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # creates a layout for the recipe info screen
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            padding=dp(10),
        )
        self.add_widget(layout)

        # adds top bar to the screen
        topBar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(
                    icon="arrow-left",
                    on_release=self.go_back,
                ),
                MDTopAppBarTitle(
                    text="Back"
                )
            ),
            md_bg_color=self.theme_cls.primaryColor,
        )
        layout.add_widget(topBar)

        # adds scroll functionality to the screen
        scroll = MDScrollView()
        layout.add_widget(scroll)

        # creates layout for the recipe info section
        recipeInfoLayout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
        )
        recipeInfoLayout.bind(minimum_height=recipeInfoLayout.setter('height'))
        scroll.add_widget(recipeInfoLayout)

        # creates a label to display the recipe name
        recipName = MDLabel(
            text=recipe.getName(),
            halign="center",
            padding=dp(10),
            adaptive_height=True,
        )
        recipeInfoLayout.add_widget(recipName)

        # display the recipe image
        recipeImage = FitImage(
            source=recipe.getImage(),
            size_hint_y=None,
            height=dp(400),
            radius=dp(24),
        )
        recipeInfoLayout.add_widget(recipeImage)

        # creates a label to display the recipe summary
        summaryLabel = MDLabel(
            text="Summary: " + recipe.getSummary(),
            markup=True,
            padding=dp(10),
            adaptive_height=True,
        )
        recipeInfoLayout.add_widget(summaryLabel)

        # display the recipe ingredients owned and missing
        # missing ingredients displayed in red
        ingredients = (
                "[color=00C853]" + ", ".join(recipe.ownedIngredients()) + "[/color]\n"
                                                                          "[color=F44336]" + ", ".join(
            recipe.missingIngredients()) + "[/color]"
        )
        # creates a label to display the recipe ingredients
        ingredientsLabel = MDLabel(
            text="Ingredients: " + ingredients,
            markup=True,
            padding=dp(10),
            adaptive_height=True,
        )
        recipeInfoLayout.add_widget(ingredientsLabel)


    def go_back(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = "Recipe Generator"


############################### PANTRY LIST SCREEN ####################################
class PantryListScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        md_list = MDList(pos_hint={'center_y': 0.7})

        if (pantry_list.getRange() == 0):
            MDListItem(MDListItemHeadlineText(
                text="Pantry is empty"
            ))
            self.add_widget(md_list)
        else:
            for i in range(pantry_list.getRange()):
                md_list_item = MDListItem(
                    MDListItemHeadlineText(
                        text=pantry_list.getItem(i).getName()
                    ),
                    MDListItemSupportingText(
                        text=pantry_list.getItem(i).getExpiration()
                    ),
                    MDListItemTrailingIcon(
                        icon="trash-can-outline"
                    )
                )
                md_list.add_widget(md_list_item)

            self.add_widget(md_list)

    def on_tap_checkbox(self):
        print("tapped checkbox")

############################### GROCERY LIST SCREEN ####################################
class GroceryListScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        searchBar = MDTextField(
            MDTextFieldHintText(text="Search for grocery item"),
            pos_hint={"center_x": 0.5, "center_y":0.9},
            size_hint_x=0.8
        )
        self.add_widget(searchBar)

        md_list = MDList(pos_hint={'center_y': 0.6})

        for i in range(grocery_list.getRange()):
            checkbox = MDListItemTrailingCheckbox(),
            md_list_item = MDListItem(
                MDListItemHeadlineText(
                    text=grocery_list.getItem(i).getName()
                ),
                MDListItemTrailingCheckbox(on_active=self.on_checkbox_active,id=str(i)),

            )
            #checkbox.bind(pressed=self.on_pressed)
            md_list.add_widget(md_list_item)

        self.add_widget(md_list)

    def on_checkbox_active(
            self,
            #screen: GroceryListScreen,
            list: MDList,
            item: MDListItem,
            item_text: str,
            item_checkbox: MDListItemTrailingCheckbox
    ):
        self.root.get_ids().screen_manager.current = item_text
        item = grocery_list.getItemFromStr(item_text)
        grocery_list.checkOff(item, pantry_list)
        print(f"checked")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(MDListItemTrailingCheckbox, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        #self.root.get_ids().screen_manager.current = item_text
        #item = grocery_list.getItemFromStr(item_text)
        #grocery_list.checkOff(item, pantry_list)
        print(f"checked")
        print('pressed at {pos}'.format(pos=pos))


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

    def build(self):
        return MDBoxLayout(
            MDScreenManager(
                BaseScreen(
                    name="Home",
                    image_size="1024",
                ),
                RecipeGenScreen(
                    name="Recipe Generator",
                ),
                PantryListScreen(
                    name="My Pantry",
                    #image_size="600",
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