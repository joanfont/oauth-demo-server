from flask import request, render_template, session
from api import models


def get_current_user():
    return models.User.query.get(session['id']) if 'id' in session else None


def access_token_handler():
    return None
