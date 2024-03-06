from flask import Blueprint,jsonify, request,render_template,session,redirect,flash
import json

#Base de datos
from db import mongo

#Mis herramientas
from tools.login import login_required

qrcode = Blueprint('qrcode',__name__)

@qrcode.route('/')
@login_required
def index():
    sub = session.get("userinfo")['sub']
    print(sub)
    resultado = mongo.db.qr.find_one({'sub':sub})

    if resultado:
        resultado['_id'] = str(resultado['_id'])

        return render_template(
            "qrcode.html",
            user = session.get("userinfo"),
            qr = resultado,
            pretty=json.dumps(session.get("user"), indent=4),
        )
    else:
        return render_template(
            "qrnotfound.html",
            user = session.get("userinfo"),
            qr = resultado,
            pretty=json.dumps(session.get("user"), indent=4),
        )
        