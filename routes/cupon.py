from flask import Blueprint,render_template,session,json,redirect,request,flash

from bson import json_util
from bson.objectid import ObjectId

#Mis herramientas
from tools.login import login_required

#DB 
from db import mongo

cupon = Blueprint('cupon',__name__)

@cupon.route('/<id>')
@login_required
def index(id):
    cupon = mongo.db.tarjeta.find_one({'_id':ObjectId(id)})
    print('Cupones')
    print(id)
    return render_template("/cupones/cupon.html",
        cupon = cupon,                 
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@cupon.route('/canje', methods = ['GET','POST'])
@login_required
def cupon_canje():
        
        if request.method == 'POST':
              
              codigo = request.form['codigo']
              result = mongo.db.tarjeta.find_one({'codigo':codigo})
              
              if result:
                    mongo.db.tarjeta.delete_one({'codigo':codigo})
                    flash('Canje exitoso', 'success')
              else:
                    flash('Error al ingresar el código', 'error')
                
              print(result)
              

                   

        return render_template("/cupones/canje.html",
        cupon = cupon,                 
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )