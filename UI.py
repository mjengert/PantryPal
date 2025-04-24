from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, Clock
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarLeadingButtonContainer, MDActionTopAppBarButton, MDTopAppBarTitle
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText, MDIconButton
from kivymd.uix.fitimage import FitImage
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)

from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDList, \
    MDListItemSupportingText, MDListItemLeadingAvatar, MDListItemTertiaryText
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from couponScreen import  CouponScreen

from recipeGenerator import RecipeGenerator
from UserData import *

#****************** Pulling Data from Database *********************#

global isLoggedIn
isLoggedIn = False

user = UserData("sample")
pantry_list = user.getPantryList()
grocery_list = user.getGroceryList()

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

############################### LOGIN SCREEN ####################################
class LoginScreen(MDScreen):
    image_size = StringProperty()
    #screen = MDScreen()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = None
        self.password = None
        self.light_primary = self.theme_cls.primaryColor[:3] + [.1]
        self.layout = MDBoxLayout(orientation='vertical')

        self.username_input = MDTextField(multiline=False, size_hint=(0.6, 0.1),
                                      pos_hint={"center_x": 0.5,"center_y": 0.4}, radius=[30, 30, 30, 30], halign="center", padding=(20, 10, 20, 10))
        self.username_input.add_widget(MDTextFieldHintText(text='Username'))
        self.username_input.bind(on_text_validate=self.login_name)

        self.password_input = MDTextField(multiline=False, size_hint=(0.6, 0.1),
                                      pos_hint={"center_x": 0.5, "center_y": 0.5}, radius=[30, 30, 30, 30], halign="center", padding=(20, 10, 20, 10), password=True)
        self.password_input.add_widget(MDTextFieldHintText(text='Password'))
        self.password_input.bind(on_text_validate=self.password_name)

        self.title = MDLabel(text="Login to PantryPal", pos_hint={"center_x": 0.5}, padding='10sp', halign='center',
                             size_hint=(1, 0.15), theme_text_color="Custom", text_color=self.theme_cls.primaryColor)
        self.title.font_size = '50sp'

        self.login_button = MDButton(
                    MDButtonText(
                        text="Login",
                    ),
                    style="elevated",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    #padding=(20, 10, 20, 10)
                )
        self.login_button.bind(on_press=self.try_login)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.login_button)

        self.add_widget(self.layout)

    def login_name(self, instance):
        self.username = self.username_input.text.strip()

    def password_name(self, instance):
        self.password = self.password_input.text.strip()

    def try_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        user = UserData(username)
        if (user.getPassword() == password):
            grocery_list = user.getGroceryList()
            pantry_list = user.getPantryList()


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
        self.md_list = MDList(
            pos_hint={'center_y': 0.7},
            size_hint=(1, None),
            height=dp(400),
        )
        scroll.add_widget(self.md_list)

        # create the recipes based on the ingredients in the pantry
        self.createRecipes()

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
        # add the missing ingredients to the grocery list
        for ingredient in recipe.missingIngredientsList():
            ig = ingredient.name
            ingredientItem = Item(ig)
            grocery_list.addToGrocery(ingredientItem)
            # display new items in grocery list; uses grocery list screen class to add items
            groceryListScreen = self.manager.get_screen("Grocery List")
            groceryListScreen.create_item_quick(ig)

    # generate the recipes based on the ingredients in the pantry and display them
    def createRecipes(self):
        # clear the list before adding new recipes
        self.md_list.clear_widgets()

        # calling the recipe generator API
        recipeGen = RecipeGenerator()

        # get the ingredients from the pantry
        ingredients = []
        for key in pantry_list.items:
            ingredients.append(key)

        # get the recipes based on the ingredients
        recipeGen.generateRecipe(ingredients)

        # get recipe info from the API
        for recipe in recipeGen.recipeList:
            recipeGen.getRecipeInfo(recipe)

        # if pantry list is empty, show default recipes
        if recipeGen.recipeList == []:
            self.md_list.add_widget(MDListItem(text='No recipes found'))

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
                        text="Owned Ingredients: " + recipe.ownedIngredientsStr()
                    ),
                    # display the recipe ingredients missing
                    MDListItemTertiaryText(
                        text="Missing Ingredients: " + recipe.missingIngredientsStr()
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
                self.md_list.add_widget(md_list_item)



    # function to remove missing ingredients from grocery list, toggle icon, and announcement
    def deleteMissingIngredients(self, instance, recipe):
       pass

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
            text=recipe.getSummary(),
            markup=True,
            padding=dp(10),
            adaptive_height=True,
        )
        recipeInfoLayout.add_widget(summaryLabel)

        # display the recipe ingredients owned and missing
        # missing ingredients displayed in red
        ingredients = (
                recipe.missingIngredientsStr()
            + ", " +
                recipe.ownedIngredientsStr()
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

        self.item_widgets = {}
        self.layout = MDBoxLayout(orientation='vertical')
        self.light_primary = self.theme_cls.primaryColor[:3] + [.1]

        self.p_scroll_view = MDScrollView(size_hint=(0.8, 0.89), pos_hint={"center_x": 0.5})
        self.p_list_layout = MDGridLayout(cols=2, spacing=10,padding=10,size_hint_y=None)
        self.p_list_layout.bind(minimum_height=self.p_list_layout.setter('height'))

        self.p_scroll_view.add_widget(self.p_list_layout)

        self.title=MDLabel(text="My Pantry",  pos_hint={"center_x": 0.5},padding='5sp', halign='center',
                                       size_hint=(1, 0.11),theme_text_color="Custom",text_color=self.theme_cls.primaryColor)
        self.title.font_size = '50sp'
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.p_scroll_view)

        self.add_widget(self.layout)

    def add_pantry_item(self, item):
        #create box to hold pantry item
        item_box = MDBoxLayout(orientation='horizontal', size_hint=(0.49, None), height=100,
                               radius=[25,25,25,25],
                               _md_bg_color=self.light_primary)

        #box to vertically stack labels
        label_box = MDBoxLayout(orientation='vertical', size_hint=(1,.9))
        item_label = MDLabel(text= item.getName(),text_color=self.theme_cls.primaryColor[:3]+[.9],halign='center')
        item_label.font_size='24sp'
        exp_label = MDLabel(text=item.getExpiration(), text_color=self.theme_cls.primaryColor[:3]+[.5],
                            halign='center')
        exp_label.font_size='10sp'

        delete_button = MDIconButton(icon='trash-can-outline',valign='center')
        delete_button.bind(on_press=lambda btn: self.delete_item(item))

        #add widgets to layout
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
            pantry_list.removePantry(item)
            del self.item_widgets[item.getName()]
            user.delFromPantryDB(item)
        # update the recipe generator screen
        recipe_gen_screen = self.manager.get_screen("Recipe Generator")
        recipe_gen_screen.createRecipes()




    def update_item(self, item):
        self.delete_item(item)
        item.calcExpiration()
        pantry_list.addToPantry(item)
        self.add_pantry_item(item)

    def add_database_items(self):
        for item in pantry_list.items.values():
            self.add_pantry_item(item)


############################### GROCERY LIST SCREEN ####################################
class GroceryListScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_widgets = {}
        self.light_primary = self.theme_cls.primaryColor[:3]+[.1]
        self.layout = MDBoxLayout(orientation='vertical')
        self.text_input = MDTextField(multiline=False, size_hint=(0.6, 0.1),
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
        self.g_list_layout = MDGridLayout(cols=2, spacing=10,size_hint_y=None)
        self.g_list_layout.bind(minimum_height=self.g_list_layout.setter('height'))

        self.g_scroll_view.add_widget(self.g_list_layout)

        self.title = MDLabel(text="Your Grocery List", pos_hint={"center_x": 0.5},padding='5sp', halign='center',
                             size_hint=(1, 0.15),theme_text_color="Custom",text_color=self.theme_cls.primaryColor)
        self.title.font_size= '50sp'
        self.layout.add_widget(self.title)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.quick_selects)
        self.layout.add_widget(self.g_scroll_view)

        self.add_widget(self.layout)


    def create_item(self, instance):
        item_name = self.text_input.text.strip()
        if item_name and item_name not in self.item_widgets:
            new_item = Item(item_name)
            grocery_list.addToGrocery(new_item)
            user.addToGrocDB(new_item)

            # create box to hold grocery item
            item_box = MDBoxLayout(orientation='horizontal', size_hint=(0.49, None),height=75,
                                   radius=[25,25,25,25],
                                   _md_bg_color=self.light_primary)
            check_button = MDIconButton(icon='check',valign='center')
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = MDLabel(text=new_item.getName(), text_color=self.theme_cls.primaryColor[:3]+[.9], pos_hint={"center_x": 0.5},
                            halign='center')

            delete_button = MDIconButton(icon='trash-can-outline', valign='center')
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            # add widgets to layout
            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''
            self.item_widgets[item_name] = item_box
    def create_item_quick(self, item_name):
        if item_name and item_name not in self.item_widgets:
            new_item = Item(item_name)
            grocery_list.addToGrocery(new_item)

            # create box to hold grocery item
            item_box = MDBoxLayout(orientation='horizontal', pos_hint={"center_y": 0.5},size_hint=(0.49, None),height=75,
                                   radius=[25,25,25,25],_md_bg_color=self.light_primary)
            check_button = MDIconButton(icon='check', valign='center',pos_hint={"center_y": 0.5})
            check_button.bind(on_press=lambda btn: self.check_off_item(new_item, item_box))

            label = MDLabel(text=new_item.getName(), text_color=self.theme_cls.primaryColor[:3]+[.9],pos_hint={"center_x": 0.5},
                            halign='center')

            delete_button = MDIconButton(icon='trash-can-outline', valign='center', pos_hint={"center_y": 0.5})
            delete_button.bind(on_press=lambda btn: self.delete_item(new_item, item_box))

            # add widgets to layout
            item_box.add_widget(check_button)
            item_box.add_widget(label)
            item_box.add_widget(delete_button)

            self.g_list_layout.add_widget(item_box)
            self.text_input.text = ''
            self.item_widgets[item_name] = item_box



    def check_off_item(self, item, item_box):
        """Moves item from grocery list to pantry list and calculates expiration date"""

        pantry_screen = self.manager.get_screen("My Pantry")
        if grocery_list.checkOff(item, pantry_list):
            self.g_list_layout.remove_widget(item_box)
            pantry_screen.add_pantry_item(item)
            user.addToPantryDB(item)
            user.delFromGrocDB(item)
        else:
            self.g_list_layout.remove_widget(item_box)
            pantry_screen.update_item(item)

    def delete_item(self, item, item_box):
        """Removes item from grocery list"""
        grocery_list.removeGrocery(item)
        self.g_list_layout.remove_widget(item_box)
        user.delFromGrocDB(item)

    def add_database_items(self):
        for item in grocery_list.items:
            self.create_item_quick(item)

        #user.addToGrocDB()
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
        self.theme_cls.primary_palette = "Red"
        self.screen_manager = MDScreenManager(
                LoginScreen(
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
                CouponScreen(
                    name="Coupons",

                ),
                id="screen_manager",
            )
        self.screen_manager.current = "Home"
        Clock.schedule_once(self._prewarm_screens, 0.1)

        return MDBoxLayout(
            self.screen_manager,
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

    def _prewarm_screens(self, dt):
        current_screen = self.screen_manager.current

        # Swap to pantry screen to force layout
        self.screen_manager.current = "My Pantry"
        self.screen_manager.current = "Coupons"
        self.screen_manager.current = "Grocery List"
        # Immediately swap back to original screen
        Clock.schedule_once(lambda dt: setattr(self.screen_manager, "current", current_screen), 0.1)

    def on_start(self):

        for store in self.screen_manager.get_screen("Coupons").coupons:
            btn = MDButton(on_release=lambda x, s=store: self.screen_manager.get_screen("Coupons").filter_coupons(s),
                           theme_width="Custom",style='outlined',height="56dp", size_hint_x=.5)
            btn.add_widget(MDButtonText(text=store,pos_hint={"center_x": 0.5, "center_y": 0.5}))  # or MDButtonText if you're using it
            self.screen_manager.get_screen("Coupons").store_buttons.add_widget(btn)

        self.screen_manager.get_screen("Coupons").filter_coupons('Target')
        self.screen_manager.get_screen("Grocery List").add_database_items()
        self.screen_manager.get_screen("My Pantry").add_database_items()


PantryPalUI().run()
