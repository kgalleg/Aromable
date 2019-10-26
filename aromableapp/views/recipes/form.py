import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category
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

def get_categories():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Category)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.name

        FROM aromableapp_category c
        """)

        return db_cursor.fetchall()

@login_required
def recipe_form(request):
    if request.method == 'GET':
        categories = get_categories()
        template = 'recipes/form.html'
        context = {
            'all_categories': categories
        }

        return render(request, template, context)


@login_required
def recipe_edit_form(request, recipe_id):
    if request.method == 'GET':
        recipe = get_recipe(recipe_id)
        categories = get_categories()

        template = 'recipes/form.html'
        context = {
            'recipe': recipe,
            'all_categories': categories
        }

        return render(request, template, context)


