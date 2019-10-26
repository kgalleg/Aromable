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
    recipe.id = _row["id"]
    recipe.name = _row["name"]
    recipe.notes = _row["notes"]
    # recipe.category_id = _row["category_id"]
    # recipe.user_id = _row["user_id"]
    # recipe.ingredients = []
    # library.books = []

    ingredient = Ingredient()
    ingredient.id = _row["id"]
    ingredient.name = _row["name"]
    ingredient.notes = _row["notes"]

    recipeingredient = RecipeIngredient()
    recipeingredient.id = _row["id"]
    # recipeingredient.quantity = _row["quantity"]
    recipeingredient.ingredient_id = _row["ingredient_id"]
    # recipeingredient.recipe_id = _row["recipe_id"]

    category = Category()
    category.id = _row["id"]
    category.name = _row["name"]


    recipe.ingredient = ingredient
    recipe.category = category

    return recipe



def get_recipe(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_recipe
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
                WHERE r.id = ?
        """, (recipe_id,))

    return db_cursor.fetchone()

def get_categories():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Category)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name
        from aromableapp_category c
        """)

        return db_cursor.fetchall()

def get_ingredients():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Ingredient)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            i.id,
            i.name,
            i.notes
        from aromableapp_ingredient i
        """)

        return db_cursor.fetchall()


@login_required
def recipe_details(request, recipe_id):
    if request.method == 'GET':
        recipe = get_recipe(recipe_id)
        template = 'recipes/detail.html'
        return render(request, template, {'recipe':recipe})

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
                        form_data['category'],
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


