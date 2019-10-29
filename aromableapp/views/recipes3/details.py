import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category, RecipeIngredient, Ingredient
from aromableapp.models import model_factory
from ..connection import Connection




def get_recipe(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:

        conn.row_factory = model_factory(Recipe)
        db_cursor = conn.cursor()
        db_cursor.execute("""
                SELECT
                    r.id recipe_id,
                    r.name recipe_name,
                    r.notes recipe_notes,
                    r.category_id,
                    c.id category_id,
                    c.name category_name,
                    ri.id recipeingredient_id,
                    ri.ingredient_id recipeingredient_ingredientid,
                    ri.recipe_id,
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


    # def get_recipes():
    #     with sqlite3.connect(Connection.db_path) as conn:
    #         conn.row_factory = model_factory(Recipe)
    #         db_cursor = conn.cursor()

    #     db_cursor.execute("""
    #         SELECT
    #                 r.id recipe_id,
    #                 r.name,
    #                 r.notes,
    #                 i.id ingredient_id,
    #                 i.name ingredient_name,
    #                 ri.id recipeingredient_id,
    #                 ri.quantity recipeingredient_quantity

    #             FROM aromableapp_recipe r
    #             JOIN aromableapp_ingredient i ON r.id = i.id
    #             JOIN aromableapp_recipeingredient ri ON r.id = i.id
    #             """)

    #     return db_cursor.fetchall()

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

#join?
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
        categories = get_categories()
        ingredients = get_ingredients()

# for ingredient in ingredients:


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


