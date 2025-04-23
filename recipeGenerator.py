import spoonacular
from spoonacular.rest import ApiException
import os
from dotenv import load_dotenv
load_dotenv()

# setting up the configuration
configuration = spoonacular.Configuration(
    host = "https://api.spoonacular.com"
)

# setting up the API key
configuration.api_key['apiKeyScheme'] = os.getenv("SPOONACULAR_API_KEY")

# This is the class that will be used to generate recipes based on the ingredients in the pantry
class RecipeGenerator:
    # initializing the recipe generator object
    def __init__(self):
        self.api_instance = spoonacular.RecipesApi(spoonacular.ApiClient(configuration))
        self.recipeList = []

    # function returns top 5 recipes based on the ingredients in the pantry
    def generateRecipe(self, ingredientsList):
        if len(ingredientsList) == 0:
            print("No ingredients found in the pantry.")
            return []
        try:
            # format ingredients into a string for the API
            ingredientsStr = ''
            for i in range(len(ingredientsList)):
                ingredientsStr += ingredientsList[i]
                # if not the last ingredient, add a comma
                if i != len(ingredientsList) - 1:
                    ingredientsStr += ','
            # calling the API to get recipes based on the ingredients
            api_response = self.api_instance.search_recipes_by_ingredients(
                ingredients=ingredientsStr,
                number=1,
                ranking=2,
                ignore_pantry=False
            )
            # if recipe gen is currntly empty, add the recipes to the list
            if len(self.recipeList) == 0:
                for recipe in api_response:
                    self.recipeList.append(Recipe(recipe))
            else:
                # if recipe gen is not empty, clear the list and add the new recipes
                self.recipeList.clear()
                for recipe in api_response:
                    self.recipeList.append(Recipe(recipe))
            print("Recipes generated based on the ingredients in the pantry.")
        except ApiException as e:
            print("Exception when calling RecipeApi->search_recipes_by_ingredients: %s\n" % e)

    # function to get the recipe list
    def getRecipeList(self):
        return self.recipeList

    # function to get recipe by id
    def getRecipeById(self, recipeId):
        for recipe in self.recipeList:
            if recipe.id == recipeId:
                return recipe
        return None

    # function to get recipe by name
    def getRecipeByName(self, recipeTitle):
        for recipe in self.recipeList:
            if recipe.title == recipeTitle:
                return recipe
        return None

    # function to get more information about the recipe
    def getRecipeInfo(self, recipe):
        if recipe is not None:
            api_response = self.api_instance.get_recipe_information(recipe.id)
            recipe.servings = api_response.servings
            recipe.cooking_time = api_response.ready_in_minutes
            # fix the summary to remove the HTML tags
            recipe.summary = api_response.summary.replace('<p>', '').replace('</p>', '')
            recipe.summary = recipe.summary.replace('<b>', '').replace('</b>', '')
            recipe.summary = recipe.summary.replace('<a>', '').replace('</a>', '')
            recipe.summary = recipe.summary.replace('<i>', '').replace('</i>', '')
            recipe.summary = recipe.summary.replace('<a', '')
            recipe.source_url = api_response.source_url
        else:
            return None

# This is the class that will be used to store the recipe information
class Recipe:
    # initializing the recipe object
    def __init__(self, recipe):
        self.id = recipe.id
        self.title = recipe.title
        self.image = recipe.image
        self.missedIngredientsList = recipe.missed_ingredients
        self.usedIngredientsList = recipe.used_ingredients
        self.missedIngredientsStr = ', '.join(
            [ing.name for ing in recipe.missed_ingredients if ing.name]
        )
        self.usedIngredientsStr = ', '.join(
            [ing.name for ing in recipe.used_ingredients if ing.name]
        )
        self.servings = 0
        self.cooking_time = 0
        self.summary = ''
        self.source_url = ''

    # function to get the recipe name
    def getName(self):
        return self.title

    # function to get the recipe image
    def getImage(self):
        return self.image

    # function to get the owned recipe ingredients as a string
    def ownedIngredientsStr(self):
        return self.usedIngredientsStr

    # function to get the missing recipe ingredients as a string
    def missingIngredientsStr(self):
        return self.missedIngredientsStr

    # function to get the owned recipe ingredients as a list
    def ownedIngredientsList(self):
        return self.usedIngredientsList

    # function to get the missing recipe ingredients as a list
    def missingIngredientsList(self):
        return self.missedIngredientsList

    # function to get the recipe id
    def getId(self):
        return self.id

    # function to get the recipe servings
    def getServings(self):
        return self.servings

    # function to get the recipe cooking time
    def getCookingTime(self):
        return self.cooking_time

    # function to get the recipe summary
    def getSummary(self):
        return self.summary

    # function to get the recipe source url
    def getSourceUrl(self):
        return self.source_url

