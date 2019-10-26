import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aromableapp.models import Ingredient
from aromableapp.models import model_factory
from ..connection import Connection


def get_ingredient(ingredient_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Ingredient)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            i.id,
            i.name,
            i.notes
        FROM aromableapp_ingredient i
        WHERE i.id = ?
        """, (ingredient_id,))

    return db_cursor.fetchone()


@login_required
def ingredient_form(request):
    if request.method == 'GET':
        template = 'ingredients/form.html'
        context = {}

        return render(request, template, context)


@login_required
def ingredient_edit_form(request, ingredient_id):
    if request.method == 'GET':
        ingredient = get_ingredient(ingredient_id)

        template = 'ingredients/form.html'
        context = {
            'ingredient': ingredient
        }

        return render(request, template, context)
