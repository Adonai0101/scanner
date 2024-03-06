from flask import Blueprint,render_template,session,json,jsonify,request
#Mis herramientas
from tools.login import login_required
from tools.tools import get_fecha
from tools.tools import generar_codigo
from bson import json_util
from bson.objectid import ObjectId

#Base de datos
from db import mongo

scaner = Blueprint('scaner',__name__)

@scaner.route('/')
@login_required
def index():
    return render_template(
        "/scaner/scaner.html",
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


#pantallas para mostar si tuvimos un error o fue exitoso
@scaner.route('/done')
@login_required
def scaner_done():
    return render_template(
        "/scaner/scaner_done.html",
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@scaner.route('/error')
@login_required
def scaner_error():
    return render_template(
        "/scaner/scaner_error.html",
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@scaner.route('/',methods = ['POST'])
def read_code():
    user = session.get("userinfo")

    code = request.json['codigo']
    print(code)
    try:
        resultado = mongo.db.qr.find_one({'_id':ObjectId(code)})
  
        if resultado: #Comprobando si existe un codigo QR registrado
            #Ahora verificamos si ya existe esta tarjeta registrada por el usuario
            consulta = mongo.db.tarjeta.find_one({'qr._id':ObjectId(code)})
            if consulta:
                filtro = {'qr._id':ObjectId(code)}
                actualizacion = {'$inc': {'canjes': 1}}
                mongo.db.tarjeta.update_one(filtro,actualizacion)
                print('Se tenemos tarjeta incrementar')
            else:
                print('no tenemos tarjeta generar una nueva')
                tarjeta = {
                    'fecha':get_fecha(),
                    'canjes':1,
                    'codigo': generar_codigo(),
                    'userID':user['_id'],
                    'qr':resultado
                }
                mongo.db.tarjeta.insert_one(tarjeta)
                print(tarjeta)
            return jsonify({'msj':'ehevh'})
        else:
            return jsonify({'msj':'caca'}),500
    except:
        print('codigo fallido')
        return jsonify({'msj':'caca'}),500