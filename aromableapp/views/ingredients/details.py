import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
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
            """, (ingredient_id,)
        )

        return db_cursor.fetchone()

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
def ingredient_details(request, ingredient_id):
    if request.method == 'GET':

        ingredient = get_ingredient(ingredient_id)
        template = 'ingredients/detail.html'
        context = {
            'ingredient': ingredient
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing an ingredient
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    UPDATE aromableapp_ingredient
                    SET name = ?,
                        notes = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['name'],
                        form_data['notes'],
                        ingredient_id,
                    )
                )

            return redirect(reverse('aromableapp:ingredients'))

        # Check if this POST is for deleting an ingredient
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM aromableapp_ingredient
                    WHERE id = ?
                """, (ingredient_id,))

            return redirect(reverse('aromableapp:ingredients'))
