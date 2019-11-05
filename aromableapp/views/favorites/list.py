import sqlite3
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Category, Recipe, Favorite
from aromableapp.models import model_factory
from ..connection import Connection

@login_required
def favorite_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Favorite)

            user = request.user

            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                f.id,
                f.recipe_id,
                f.user_id
            from aromableapp_favorite f
            WHERE f.user_id = ?
            """, (user.id,))

        all_favorite_recipes = db_cursor.fetchall()

        template_name = 'favorites/list.html'

        context = {'all_favorites': all_favorite_recipes,}

        return render(request, template_name, context)

#POST data submitted; process data
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:

            db_cursor = conn.cursor()

    # ??? are placeholders to validate parameters
            db_cursor.execute("""
            INSERT INTO aromableapp_favorite
            (
                user_id,
                recipe_id
            )
            VALUES (?, ?)
            """,
            # this is the second argument which is the data dictionary
            (request.user.id, form_data['recipe_id']))

# this is now a GET request from the redirect
        return redirect(reverse('aromableapp:favorites'))
