from flask import Blueprint

bp = Blueprint('game', __name__,
              template_folder='templates',
              static_folder='static',
              static_url_path='/static')

from gemfarm.game import routes