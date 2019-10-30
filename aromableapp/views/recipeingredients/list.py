import sqlite3
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection

@login_required
def recipeingredient_list(request):
    if request.method == 'POST':
        form_data = request.POST
        ingredient_id = request.POST.getlist('checkbox[]')


        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            for id in ingredient_id:
                db_cursor.execute("""
                INSERT INTO aromablerapp_recipeingredient
                (
                    ingredient_id, recipe_id
                )
                VALUES (?, ?)
                """,
                (form_data['recipe_id'], id,)
                )

        return redirect(reverse('aromableapp:recipe'))