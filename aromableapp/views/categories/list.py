import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Category
from aromableapp.models import model_factory
from ..connection import Connection


def create_category(cursor, row):
    _row = sqlite3.Row(cursor, row)

    category = Category()
    category.id = _row["id"]
    category.name = _row["name"]

    return (category,)



@login_required
def category_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            user = request.user

            conn.row_factory = model_factory(Category)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.id,
                c.name
            from aromableapp_category c
            where user_id = ?
            """, (user.id,))


            all_categories = db_cursor.fetchall()

        template_name = 'categories/list.html'
        return render(request, template_name, {'all_categories': all_categories})

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO aromableapp_category(name, user_id)
            values (?, ?)
            """,
            (form_data['name'], request.user.id))

        return redirect(reverse('aromableapp:categories'))