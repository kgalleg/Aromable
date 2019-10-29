import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category, Ingredient
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
            r.notes
        FROM aromableapp_recipe r
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
            i.name
        from aromableapp_ingredient i
        """)

        return db_cursor.fetchall()








@login_required
def recipe_form(request):
    if request.method == 'GET':
        categories = get_categories()
        ingredients = get_ingredients()
        template = 'recipes/form.html'
        context = {
            'all_categories': categories,
            'all_ingredients': ingredients
        }

        return render(request, template, context)


@login_required
def recipe_edit_form(request, recipe_id):
    if request.method == 'GET':
        recipe = get_recipe(recipe_id)

        template = 'recipes/form.html'
        context = {
            'recipe': recipe
        }

        return render(request, template, context)