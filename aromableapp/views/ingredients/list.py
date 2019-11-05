import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Ingredient
from aromableapp.models import model_factory
from ..connection import Connection

@login_required
def create_ingredient(cursor, row):
    _row = sqlite3.Row(cursor, row)

    ingredient = Ingredient()
    ingredient.id = _row["id"]
    ingredient.name = _row["name"]
    ingredient.notes = _row["notes"]


    return (ingredient,)


@login_required
def ingredient_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:



            conn.row_factory = model_factory(Ingredient)
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    i.id,
                    i.name,
                    i.notes,
                    i.user_id
                FROM aromableapp_ingredient i
                where i.user_id = ?
            """, (request.user.id,))

            all_ingredients = db_cursor.fetchall()

        template = 'ingredients/list.html'
        return render(request, template, {'all_ingredients': all_ingredients})

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                INSERT INTO aromableapp_ingredient(name, notes, user_id)
                VALUES (?, ?, ?)
                """,
                (form_data['name'],
                form_data['notes'],
                request.user.id)
            )

        return redirect(reverse('aromableapp:ingredients'))