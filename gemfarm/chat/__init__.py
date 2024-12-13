from flask import Blueprint

bp = Blueprint('chat', __name__)

from gemfarm.chat import events
