import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection


def get_recipes():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            r.id,
            r.name,
            r.notes,
            r.category_id,
            r.user_id
        FROM aromableapp_recipe r
        """)

        return db_cursor.fetchall()


def get_ingredients():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
         select
            ri.id,
            ri.name,
            ri.notes
        from aromableapp_ingredient i
        """)

        return db_cursor.fetchall()

@login_required
def recipeingredient_form(request):
    if request.method == 'GET':
        ingredients = get_ingredients()
        recipes= get_recipes()
        template = 'recipes/form.html'
        context = {
            'all_recipes': recipes,
            'all_ingredients': ingredients
        }

        return render(request, template, context)