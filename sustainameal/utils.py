from collections import Counter
import ast
from sklearn.preprocessing import StandardScaler

def calculate_normalized_nutrient_centroid(recipe_indices, recipes_df, nutrients, vectorizer):
    """
    Calculates the normalized nutrient centroid for a set of recipes using the NutritionVectorizer.

    Args:
    recipe_indices (list of int): List of recipe IDs.
    recipes_df (pandas.DataFrame): DataFrame containing the recipes.
    nutrients (list of str): List of nutrient names to use for the centroid calculation.
    vectorizer (NutritionVectorizer): Instance of NutritionVectorizer used for normalizing nutrient data.

    Returns:
    numpy.ndarray: Normalized nutrient centroid vector for the provided recipes.
    """

    # Filter the DataFrame for the specified recipe IDs
    filtered_recipes = recipes_df[recipes_df['recipe_id'].isin(recipe_indices)]
    # Extract the nutrient values of interest
    nutrient_data = filtered_recipes[nutrients]

    # Normalize the nutrient data using the transform method of NutritionVectorizer
    normalized_nutrient_data = vectorizer.transform(nutrient_data)

    # Calculate the normalized nutrient centroid
    centroid = normalized_nutrient_data.mean(axis=0)

    centroid_array = centroid.to_numpy()
    centroid_array = centroid_array.reshape(1, -1)

    return centroid_array



def calculate_centroid_and_find_common_tags(similar_recipes, recipes_df, nutrient_vectors_df, vectorizer):
    """
    Calculates the nutritional centroid and finds the most common tags for a set of similar recipes.

    Args:
    similar_recipes (list of tuples): List of tuples (recipe_id, title, similarity).
    recipes_df (pandas.DataFrame): DataFrame containing recipe data.
    nutrient_vectors_df (pandas.DataFrame): DataFrame of normalized nutritional vectors.

    Returns:
    numpy.ndarray: Nutritional centroid vector.
    list: List of the 6 most common tags.
    """
    # Extract the recipe IDs
    recipe_ids = [recipe[0] for recipe in similar_recipes]

    # Calculate the centroid of the nutritional values
    centroid = calculate_normalized_nutrient_centroid(recipe_ids, recipes_df, nutrient_vectors_df, vectorizer)

    # Find all tags for the similar recipes
    all_tags = []
    for recipe_id in recipe_ids:
        tags = recipes_df.loc[recipes_df['recipe_id'] == recipe_id, 'tags'].values[0]
        if isinstance(tags, str):
            # Convert the string of tags into a list if necessary
            tags = eval(tags)
        all_tags.extend(tags)

    # Count the frequency of each tag and find the 6 most common
    most_common_tags = [tag for tag, count in Counter(all_tags).most_common(6)]

    return centroid, most_common_tags
