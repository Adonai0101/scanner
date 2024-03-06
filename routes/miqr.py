from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json

#Base de datos
from db import mongo

#Mis herramientas
from tools.login import login_required
from tools.validaciones import *

miqr = Blueprint('miqr',__name__)

@miqr.route('/')
@login_required
def index():
    user = session.get("userinfo")
    qr = mongo.db.qr.find_one({'sub':user['sub']})

    return render_template(
        "configcode.html",
        user = session.get("userinfo"),
        qr = qr,
        pretty=json.dumps(session.get("user"), indent=4),
    )


@miqr.route('/',methods = ['POST'])
@login_required
def create():
    user = session.get("userinfo")

    try:
        datos = {
            'sub': user['sub'],
            'canjes': int(request.form['canjes']),
            'recompensa': request.form['recompensa'],
            'user':user
        }
        if datos['canjes'] > 10:
            flash('El número de canjes no puede ser mas de 10','error')
            return redirect('/miqr')
    except: #Validamos que en realidad se ingrese un numero en los canjes
        flash('Error al ingresar los datos','error')
        return redirect('/miqr')

    if solo_numeros(request.form['canjes']) and is_nombre(request.form['recompensa']):

        resultado = mongo.db.qr.find_one({'sub':user['sub']})
        #Coprobamos si existe 
        if resultado:
            #Actuzalizando mi QR
            mongo.db.qr.update_one({'sub':user['sub']},{"$set":datos})
            #actualizando las tarjetas
            mongo.db.tarjeta.update_many({'qr.user.sub':user['sub']},{"$set":{
                'qr.canjes':datos['canjes'],
                'qr.recompensa':datos['recompensa'],
            }})
            flash('Tarjeta actualizada','success')

        else:
            mongo.db.qr.insert_one(datos)
            flash('Tarjeta registrada','success')
    else:
        flash('Error al ingresar los datos','error')

    return redirect('/miqr')