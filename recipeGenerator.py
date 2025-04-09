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

class RecipeGenerator:
    def __init__(self):
        self.api_instance = spoonacular.RecipesApi(spoonacular.ApiClient(configuration))

    # function returns top 5 recipes based on the ingredients provided
    def generateRecipe(self, ingredients):
        try:
            # calling the API to get recipes based on the ingredients
            api_response = self.api_instance.search_recipes_by_ingredients(
                ingredients=ingredients,
                number=5,
                ranking=2,
                ignore_pantry=False
            )
            return api_response
        except ApiException as e:
            print("Exception when calling RecipeApi->generate_recipes_by_ingredients: %s\n" % e)

