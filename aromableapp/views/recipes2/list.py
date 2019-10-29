import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Ingredient, RecipeIngredient
from aromableapp.models import model_factory
from ..connection import Connection


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
            r.category_id,
            r.user_id
        FROM aromableapp_recipe r
        """)


            all_recipes = db_cursor.fetchall()


        template = 'recipes/list.html'
        return render(request, template, {'all_recipes': all_recipes})

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                INSERT INTO aromableapp_recipe (name, notes, category_id, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (form_data['name'], form_data['notes'],
                request.user.id,form_data['category']))

        return redirect(reverse('aromableapp:recipes'))


