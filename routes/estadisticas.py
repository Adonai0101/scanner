from flask import Blueprint,jsonify, request

#Mis herramientas
from tools.login import login_required

estadisticas = Blueprint('estadisticas',__name__)

@estadisticas.route('/')
@login_required
def index():
    return "Mi Estadisticas"