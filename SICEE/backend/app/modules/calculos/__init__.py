from flask import Blueprint

bp = Blueprint('calculos', __name__)

from . import routes # noqa: E402,F401
