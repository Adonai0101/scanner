from flask import Blueprint,render_template,session,json,redirect

from bson import json_util
from bson.objectid import ObjectId

#Mis herramientas
from tools.login import login_required

#DB 
from db import mongo

tarjetas = Blueprint('tarjetas',__name__)

@tarjetas.route('/')
@login_required
def index():

    user = session.get("userinfo")
    user_id = user['_id']

    tarjetas = mongo.db.tarjeta.find({'userID':user_id})
    lista = list(tarjetas)

    return render_template("/usuario/tarjetas.html",
        tarjetas = lista,                   
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@tarjetas.route('/<id>')
@login_required
def one_card(id):

    try:
        tarjeta = mongo.db.tarjeta.find_one({'_id':ObjectId(id)})
        print(tarjeta)

        return render_template("/usuario/tarjeta.html",
            tarjeta = tarjeta,                 
            session=session.get("user"),
            user = session.get("userinfo"),
            pretty=json.dumps(session.get("user"), indent=4),
        )
    except:
        print('no es valido')
        return redirect('/404')
    