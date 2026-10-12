from flask import Blueprint

ibp = Blueprint('investigadores', __name__)

from . import routes # noqa: E402,F401