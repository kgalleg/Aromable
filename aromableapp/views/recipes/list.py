import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Ingredient, RecipeIngredient
from aromableapp.models import model_factory
from ..connection import Connection


def create_recipe(cursor, row):
    _row = sqlite3.Row(cursor, row)

    recipe = Recipe()
    recipe.id = _row["id"]
    recipe.name = _row["name"]
    recipe.notes = _row["notes"]
    recipe.ingredients = []
    # library.books = []

    ingredient = Ingredient()
    ingredient.id = _row["ingredient_id"]
    ingredient.name = _row["ingredient_name"]

    recipeingredient = RecipeIngredient()
    recipeingredient.id = _row["recipeingredient_id"]
    recipeingredient.quantity = _row["recipeingredient_quantity"]



    return (recipe, ingredient,)


@login_required
def recipe_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Recipe)
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    r.id,
                    r.name,
                    r.notes,
                    i.id ingredient_id,
                    i.name ingredient_name,
                    ri.id recipeingredient_id,
                    ri.quantity recipeingredient_quantity
                FROM aromableapp_recipe r
                JOIN aromableapp_ingredient i ON r.id = i.id
                JOIN aromableapp_recipeingredient ri ON r.id = i.id
            """)

            recipes = db_cursor.fetchall()

            #starts with empty dictionary
            recipe_groups = {}

         # Iterate the list of tuples
            for (recipe, ingredient) in recipes:

                  # If the dictionary does have a key of the current
            # department 'id' value, add the key and set the
            # value to the current library
                if recipe.id not in recipe_groups:
                    recipe_groups[recipe.id] = recipe
                    recipe_groups[recipe.id].ingredients.append(ingredient)

                     # If the key does exist, just append the current employee
            # to the list of employees for the current department
                else:
                    recipe_groups[recipe.id].ingredients.append(ingredient)

        template = 'recipes/list.html'
        context = {
            'all_recipes': recipe_groups.values()
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                INSERT INTO aromableapp_recipe (name, notes)
                VALUES (?, ?)
                """,
                (form_data['name'], form_data['notes'],)
            )

        return redirect(reverse('aromableapp:recipes'))