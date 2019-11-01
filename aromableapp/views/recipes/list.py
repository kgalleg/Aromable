import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Recipe, Category
from aromableapp.models import model_factory
from ..connection import Connection



@login_required
def recipe_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            user = request.user

            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
               SELECT
                    r.id recipe_id,
                    r.name recipe_name,
                    r.notes recipe_notes,
                    c.name category_name,
                    c.id category_id


                FROM aromableapp_recipe r
                left JOIN aromableapp_category c ON r.category_id = c.id
                where user_id = ?
            """, (user.id,))


            all_recipes = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                recipe = Recipe()
                recipe.name = row['recipe_name']
                recipe.id = row['recipe_id']

                category = Category()
                category.name = row['category_name']
                category.id = row ['category_id']

                recipe.category = category

                all_recipes.append(recipe)

        template = 'recipes/list.html'
        context = {
            'all_recipes': all_recipes
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
                INSERT INTO aromableapp_recipe (name, category_id, notes, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (form_data['name'], form_data['category'], form_data['notes'],
                request.user.id,)
            )
        # with sqlite3.connect(Connection.db_path) as conn:
        #     db_cursor = conn.cursor()

            db_cursor.execute("""
                select last_insert_rowid()
                """
            )

            new_recipe_id = db_cursor.fetchone()
            tupleid = new_recipe_id[0]

        with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                for id in request.POST.getlist('ingredient[]'):

                    db_cursor.execute("""
                        INSERT INTO aromableapp_recipeingredient
                        (
                            ingredient_id, recipe_id
                        )
                        VALUES (?, ?)
                        """,
                        (id, tupleid)
                        )



        return redirect(reverse('aromableapp:recipes'))