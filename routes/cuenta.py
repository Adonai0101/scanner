from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json
#Mis herramientas
from tools.login import login_required
from tools.create_user import get_user
from tools.validaciones import *

#Base de datos
from db import mongo

cuenta = Blueprint('cuenta',__name__)

@cuenta.route('/')
@login_required
def index():
    return render_template(
        "/usuario/perfil.html",
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@cuenta.route('/',methods = ['POST'])
@login_required
def cuenta_post():
    user_session = session.get("user")
    sub =  user_session['userinfo']['sub']
    user = {
        'nombre': request.form['nombre'],
        'telefono': request.form['telefono']
    }

    #Validando los datos

    if is_nombre(user['nombre']) and is_telefono(user['telefono']):
    
        resultado = mongo.db.usuarios.update_one({'sub':sub},{"$set":user}) #revisar esta linea de codigo puede traer confligto 

        #modificando la informacion del qr segun el usuario
        resultado = mongo.db.qr.update_one({'sub':sub},{"$set":{
            'user.nombre':user['nombre'],
            'user.telefono':user['telefono'],
            }})

        #Faltaria tambien Modificar Las tarjetas de los usuarios que tengan nuestro usuario
        mongo.db.tarjeta.update_many({'qr.user.sub':sub},{"$set":{
            'qr.user.nombre':user['nombre'],
            'qr.user.telefono':user['telefono'],
        }})
        get_user()

        flash('¡Usuario modificado con éxito!', 'success')
    else:
        flash('¡Error al ingresar los datos!', 'error')
    return redirect('/cuenta')

@cuenta.route('/updatefoto',methods = ['POST'])
def update_foto():

    user = session.get("userinfo")

    user_session = session.get("user")
    sub =  user_session['userinfo']['sub']

    data = request.json
    resultado = mongo.db.usuarios.update_one({'sub':sub},{"$set":{'foto':data['url']}})
    get_user()
    flash('¡Foto actualizada!', 'success')

    return "foto actualizada"

