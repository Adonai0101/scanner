from flask import Blueprint, request, jsonify,send_from_directory,session
from werkzeug.utils import secure_filename
import os



fileserver = Blueprint('file',__name__)

@fileserver.route('/')
def index():
    return "file server"


@fileserver.route("/upload", methods=["POST"])
def upload_image():

    user = session.get("userinfo")
    print("si entro el post")
    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    if file:
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        filename = user['sub']+ "." + extension
        try:
            file.save(os.path.join("uploads", filename))
            image_url = f"{request.host_url}fileserver/imagen/{filename}"
            return jsonify({
                "message": "Imagen subida exitosamente",
                'url':image_url,
                'filename':filename
            }), 200
        except Exception as e:
            print({"error": str(e)})
            return jsonify({"error": str(e)}), 500  # Devuelve un mensaje de error y código 500 en caso de un error



@fileserver.route("/delete/<filename>", methods=["DELETE"])
def delete_image(filename):
    try:
        os.remove(os.path.join("uploads", filename))
        return jsonify({"message": "Imagen eliminada exitosamente"}), 200
    except FileNotFoundError:
        return jsonify({"error": "La imagen no existe"}), 404



@fileserver.route("/imagen/<filename>", methods=["GET"])
def obtener_imagen(filename):
    try:
        # Obtener la ruta completa del archivo
        filepath = os.path.join("uploads", filename)

        # Verificar si el archivo existe
        if not os.path.isfile(filepath):
            return jsonify({"error": "La imagen no existe"}), 404

        # Enviar la imagen como respuesta
        return send_from_directory("uploads", filename), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
