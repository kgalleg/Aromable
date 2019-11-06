import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category, Ingredient, RecipeIngredient
from aromableapp.models import model_factory
from ..connection import Connection


def get_recipe(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Recipe)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.name,
            r.notes,
            r.category_id,
            r.user_id
        FROM aromableapp_recipe r
        WHERE r.id = ?
        """, (recipe_id,))

    return db_cursor.fetchone()

@login_required
def get_categories(request):
    with sqlite3.connect(Connection.db_path) as conn:

        conn.row_factory = model_factory(Category)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.user_id

        from aromableapp_category c
        where c.user_id = ?
        """, (request.user.id,))


        return db_cursor.fetchall()

@login_required
def get_ingredients(request):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Ingredient)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            i.id,
            i.name,
            i.notes,
            i.user_id

        from aromableapp_ingredient i
        where i.user_id = ?
        """, (request.user.id,))

        return db_cursor.fetchall()


@login_required
def recipe_form(request):
    if request.method == 'GET':

        categories = get_categories(request)
        ingredients = get_ingredients(request)

        template = 'recipes/form.html'
        context = {
            'all_categories': categories,
            'all_ingredients': ingredients
        }

        return render(request, template, context)

def get_recipeingredients(recipe_id):
    with sqlite3.connect(Connection.db_path) as conn:
        # conn.row_factory = model_factory(RecipeIngredient)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            ri.ingredient_id ri_ingredient_id
        from aromableapp_recipeingredient ri
        WHERE ri.recipe_id = ?
        """,(recipe_id,))

        ingredient_ids=[]
        ingredientslist = db_cursor.fetchall()

        for i in ingredientslist:
            ingredient_ids.append(i[0])

        return ingredient_ids






@login_required
def recipe_edit_form(request, recipe_id):
    if request.method == 'GET':
        recipe = get_recipe(recipe_id)
        categories = get_categories(request)
        ingredients = get_ingredients(request)
        recipeingredients = get_recipeingredients(recipe_id)

        template = 'recipes/form.html'
        context = {
            'recipe': recipe,
            'all_categories': categories,
            'all_ingredients': ingredients,
            'recipeingredients': recipeingredients,
        }

        return render(request, template, context)