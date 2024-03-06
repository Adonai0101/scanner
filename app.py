
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from flask import Flask, redirect, render_template, session, url_for,send_from_directory

#Base de datos
from db import mongo

#Mis herramientas
from tools.login import login_required
from tools.create_user import create_user

#Blueprints
from routes.cuenta import cuenta
from routes.miqr import miqr
from routes.estadisticas import estadisticas
from routes.qrcode import qrcode
from routes.fileserver import fileserver 
from routes.scaner import scaner
from routes.tarjetas import tarjetas
from routes.cupon import cupon

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
app.secret_key = "Noquierounasecretkey"
app.config["UPLOAD_FOLDER"] = "uploads"

#Configuracion de variables de entorno

AUTH0_CLIENT_ID = env.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
APP_SECRET_KEY = "sndfbehsagv"
URL_DB = env.get("URL_DB")

app.config['MONGO_URI'] = URL_DB
mongo.init_app(app)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id = AUTH0_CLIENT_ID,
    client_secret = AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
)


#Registro de blueprints
app.register_blueprint(cuenta, url_prefix='/cuenta')
app.register_blueprint(miqr, url_prefix='/miqr')
app.register_blueprint(qrcode, url_prefix='/qrcode')
app.register_blueprint(estadisticas, url_prefix='/estadisticas')
app.register_blueprint(fileserver, url_prefix='/fileserver')
app.register_blueprint(scaner, url_prefix='/scaner')
app.register_blueprint(tarjetas, url_prefix='/tarjetas')
app.register_blueprint(cupon, url_prefix='/cupon')


@app.route("/")
@login_required
def home():
    create_user()
    
    tarjetas = mongo.db.qr.find()
    tarjetas = list(tarjetas)
    print(tarjetas)
    

    return render_template(
        "home.html",
        tarjetas = tarjetas,
        session=session.get("user"),
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    print('entramos al callbck')
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login")
def login():
    print('entramos al login')
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )


#ruta para servir recursos de static
@app.route('/imagenes/<path:nombre_imagen>')
def servir_imagen(nombre_imagen):
    return send_from_directory('static', nombre_imagen)



@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template(
        "404.html",
        user = session.get("userinfo"),
        pretty=json.dumps(session.get("user"), indent=4),
    ),404

#Terminos y condiciones template
@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True, port=5000)