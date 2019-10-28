from .auth.logout import logout_user
from .auth.register import register_user

from .home import home

from .connection import Connection

from .categories.list import category_list
from .categories.details import category_details
from .categories.form import category_form, category_edit_form

from .recipes.list import recipe_list
from .recipes.details import recipe_details
from .recipes.form import recipe_form, recipe_edit_form

from .ingredients.form import ingredient_form, ingredient_edit_form
from .ingredients.details import ingredient_details
from .ingredients.list import ingredient_list