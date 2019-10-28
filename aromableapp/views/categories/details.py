import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from aromableapp.models import Category
from aromableapp.models import model_factory
from ..connection import Connection


def get_category(category_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Category)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                i.id,
                i.name

            FROM aromableapp_category i
            WHERE i.id = ?
            """, (category_id,)
        )

        return db_cursor.fetchone()

def get_categories():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Category)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            i.id,
            i.name
        from aromableapp_category i
        """)

        return db_cursor.fetchall()


@login_required
def category_details(request, category_id):
    if request.method == 'GET':

        category = get_category(category_id)
        template = 'categories/detail.html'
        context = {
            'category': category
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing an category
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    UPDATE aromableapp_category
                    SET name = ?

                    WHERE id = ?
                    """,
                    (
                        form_data['name'],

                        category_id,
                    )
                )

            return redirect(reverse('aromableapp:categories'))

        # Check if this POST is for deleting a category
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM aromableapp_category
                    WHERE id = ?
                """, (category_id,))

            return redirect(reverse('aromableapp:categories'))
