import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category, RecipeIngredient, Ingredient
from aromableapp.models import model_factory
from ..connection import Connection

def create_recipe(cursor, row):
    _row = sqlite3.Row(cursor, row)

    recipe = Recipe()
    recipe.id = _row["recipe_id"]
    recipe.name = _row["recipe_name"]
    recipe.notes = _row["recipe_notes"]

    category = Category()
    category.id = _row["category_categoryid"]
    category.name = _row["category_name"]

    recipeingredient = RecipeIngredient()
    recipeingredient.id = _row["recipeingredient_id"]
    recipeingredient.ingredient_id = _row["recipeingredient_ingredientid"]
    recipeingredient.recipe_id = _row["recipeingredient_recipeid"]
    recipeingredient.quantity = _row["quantity_drops"]

    ingredient = Ingredient()
    ingredient.id = _row["ingredient_id"]
    ingredient.name = _row["ingredient_name"]


    recipe.ingredient = ingredient
    recipe.category = category
    recipe.recipeingredient = recipeingredient

    return recipe


def get_recipe(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:
        # conn.row_factory = model_factory(Recipe)
        # conn.row_factory = sqlite3.Row
        conn.row_factory = create_recipe
        db_cursor = conn.cursor()

        db_cursor.execute("""
                SELECT
                    r.id recipe_id,
                    r.name recipe_name,
                    r.notes recipe_notes,
                    r.category_id recipe_category_id,
                    c.id category_categoryid,
                    c.name category_name,
                    ri.id recipeingredient_id,
                    ri.ingredient_id recipeingredient_ingredientid,
                    ri.recipe_id recipeingredient_recipeid,
                    ri.quantity quantity_drops,
                    i.id ingredient_id,
                    i.name ingredient_name

                FROM aromableapp_recipe r
                left JOIN aromableapp_category c ON r.category_id = c.id
                left JOIN aromableapp_recipeingredient ri ON r.id = ri.id
                left JOIN aromableapp_ingredient i ON ri.ingredient_id = i.id
                WHERE r.id = ?
        """, (recipe_id,))

        return db_cursor.fetchone()


@login_required
def recipe_details(request, recipe_id):
    if request.method == 'GET':
        recipe = get_recipe(recipe_id)
        template = 'recipes/detail.html'
        context = {
            'recipe': recipe
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a recipe
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    UPDATE aromableapp_recipe
                    SET name = ?,
                        notes = ?,
                        category_id = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['name'],
                        form_data['notes'],
                        # form_data['category_id'],
                        recipe_id,
                    )
                )

            return redirect(reverse('aromableapp:recipes'))

        # Check if this POST is for deleting a recipe
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM aromableapp_recipe
                    WHERE id = ?
                """, (recipe_id,))

            return redirect(reverse('aromableapp:recipes'))


