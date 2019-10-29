def create_recipe(cursor, row):
    _row = sqlite3.Row(cursor, row)

    recipe = Recipe()
    recipe.id = _row["recipe_id"]
    recipe.name = _row["name"]
    recipe.notes = _row["notes"]

    # recipe.category_id = _row["category_id"]
    # recipe.user_id = _row["user_id"]
    # recipe.ingredients = []
    # library.books = []
    recipe.categories = []

    ingredient = Ingredient()
    ingredient.id = _row["ingredient_id"]
    ingredient.name = _row["ingredient_name"]
    ingredient.notes = _row["notes"]

    recipeingredient = RecipeIngredient()
    recipeingredient.id = _row["recipeingredient_id"]
    # recipeingredient.quantity = _row["quantity"]
    recipeingredient.ingredient_id = _row["ingredient_id"]
    # recipeingredient.recipe_id = _row["recipe_id"]

    category = Category()
    category.id = _row["category_id"]
    category.name = _row["category_name"]


    recipe.ingredient = ingredient
    recipe.category = category

    return recipe