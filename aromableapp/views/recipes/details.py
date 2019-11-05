import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category, RecipeIngredient, Ingredient, Favorite
from aromableapp.models import model_factory
from ..connection import Connection

def create_recipe(cursor, row):
    _row = sqlite3.Row(cursor, row)

    recipe = Recipe()
    recipe.id = _row["recipe_id"]
    recipe.name = _row["recipe_name"]
    recipe.notes = _row["recipe_notes"]
    recipe.category_id = _row["recipe_category_id"]

    category = Category()
    category.id = _row["category_categoryid"]
    category.name = _row["category_name"]

    recipeingredient = RecipeIngredient()
    recipeingredient.recipe_id = _row["ri_recipe_id"]
    recipeingredient.ingredient_id = _row["ri_ingredient_id"]
    recipeingredient.quantity = _row["quantity_drops"]

    ingredient = Ingredient()
    ingredient.name = _row["ingredient_name"]


    recipe.ingredient = ingredient
    recipe.category = category
    recipe.recipeingredient = recipeingredient

    return recipe


def get_recipe(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:

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
                    ri.quantity quantity_drops,
                    i.name ingredient_name

                FROM aromableapp_recipe r
                left JOIN aromableapp_category c ON r.category_id = c.id
                left JOIN aromableapp_recipeingredient ri ON r.id = ri.recipe_id
                left JOIN aromableapp_ingredient i ON ri.ingredient_id = i.id
                WHERE r.id = ?
        """, (recipe_id,))

        return db_cursor.fetchall()

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

def get_recipeingredients():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(RecipeIngredient)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            ri.id,
            ri.recipe_id ri_recipe_id,
            ri.ingredient_id ri_ingredient_id
        from aromableapp_recipeingredient ri
        """)

        return db_cursor.fetchall()



@login_required
def recipe_details(request, recipe_id):
    if request.method == 'GET':
        # recipe = get_recipe(recipe_id)
        recipe = Recipe.objects.get(pk=recipe_id)

        try:
            is_favorited = Favorite.objects.get(recipe_id=recipe_id, user_id=request.user.id)
        except Favorite.DoesNotExist:
            is_favorited = None

        template = 'recipes/detail.html'

        context = {
            'recipe': recipe,
            'favorited': is_favorited is None
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
                        form_data['category'],
                        recipe_id,
                    )
                )


            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                # all_recipeingredients = get_recipeingredients()

                # for recipeingredients in all_recipeingredients:
                    # if recipeingredients.recipe_id == recipe_id:

                db_cursor.execute("""
                    DELETE FROM aromableapp_recipeingredient

                    WHERE recipe_id = ?
                    """,
                    (recipe_id,)
                    )

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                for id in request.POST.getlist('ingredient[]'):

                    db_cursor.execute("""
                        INSERT INTO aromableapp_recipeingredient
                        (
                            ingredient_id, recipe_id
                        )
                        VALUES (?, ?)
                        """,
                        (id, recipe_id,)
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


