import sqlite3
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Category, Recipe, Favorite
from aromableapp.models import model_factory
from ..connection import Connection

@login_required
def favorite(request, recipe_id):
    if request.method == 'POST':
        form_data = request.POST


        # Check if this POST is for deleting a recipe from favorites for the current user
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM aromableapp_favorite
                    WHERE recipe_id = ?
                    AND user_id = ?
                """, (recipe_id, request.user.id))

            return redirect(reverse('aromableapp:favorites'))