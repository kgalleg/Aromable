import sqlite3
from django.shortcuts import render
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
        """, (category_id,))

    return db_cursor.fetchone()


@login_required
def category_form(request):
    if request.method == 'GET':
        template = 'categories/form.html'
        context = {}

        return render(request, template, context)


@login_required
def category_edit_form(request, category_id):
    if request.method == 'GET':
        category = get_category(category_id)

        template = 'categories/form.html'
        context = {
            'category': category
        }

        return render(request, template, context)
