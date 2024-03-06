from flask import session
#Base de datos
from db import mongo

def get_user():

    user_session = session.get("user")
    sub =  user_session['userinfo']['sub']

    #generando la informacion del usuario para mostrar en interfaz
    resultado = mongo.db.usuarios.find_one({'sub':sub})
    resultado['_id'] = str(resultado['_id'])
    session["userinfo"] = resultado

def create_user():
    user_session = session.get("user")
    sub =  user_session['userinfo']['sub']

    resultado = mongo.db.usuarios.find_one({'sub':sub})
    if  not resultado:
        usuario = {
            'nombre':user_session['userinfo']['nickname'],
            'email':user_session['userinfo']['email'],
            'foto':user_session['userinfo']['picture'],
            'sub':sub,
            'keyFoto':'',
            'telefono':''
        }
        user = mongo.db.usuarios.insert_one(usuario)

    #generando la informacion del usuario para mostrar en interfaz
    get_user()
    #resultado = mongo.db.usuarios.find_one({'sub':sub})
    #resultado['_id'] = str(resultado['_id'])
    #session["userinfo"] = resultado
