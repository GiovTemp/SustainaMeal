# test_sustainameal.py
import pandas as pd
from sustainameal import SustainaMeal


def test_find_similar_recipes():
    recipes_df = pd.read_csv("data/pp_recipes.csv")

    ingredients_df = pd.read_csv("data/cfp_wfp_ingredients.csv", sep=';')
    ingredients_df = ingredients_df.dropna()

    # Creazione dell'istanza di SustainaMeal
    sustainameal = SustainaMeal(
        recipes_df[:1000],
        ingredients_df,
        ['calories [cal]', 'totalFat [g]', 'saturatedFat [g]', 'cholesterol [mg]', 'sodium [mg]', 'dietaryFiber [g]',
         'sugars [g]', 'protein [g]'],
        'davanstrien/autotrain-recipes-2451975973'
    )

    similar_recipes_by_title = sustainameal.get_similar_by_title('Barbecued Roast Beef', 10)
    print(similar_recipes_by_title)
    similar_recipes = sustainameal.find_similar_recipes('Barbecued Roast Beef', 10,
                                                        acceptable_tags=['appetizers', 'main-dish', 'side-dishes',
                                                                         'fruits', 'desserts',
                                                                         'breakfast', 'pasta-rice-and-grains',
                                                                         'beverages', 'drinks'],
                                                        match_all_tags=False)

    print(similar_recipes)

    ordered_recipes = sustainameal.order_recipe_by_healthiness()
    ordered_recipes_sus = sustainameal.order_recipe_by_sustainability()

    print(ordered_recipes)
    print(ordered_recipes_sus)


# Esecuzione del test
if __name__ == "__main__":
    test_find_similar_recipes()
    print("Test completato con successo!")
