import cloudinary
import cloudinary.uploader
import cloudinary.api

#variables de entorno
from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

cloudinary.config( 
  cloud_name = env.get('CLOUD_NAME'), 
  api_key = env.get('API_KEY'), 
  api_secret = env.get('API_SECRET') 
)


def destroy_image(key):

  try:
    rest = cloudinary.uploader.destroy(key)
    print("imagen eliminada")
  except :
      print('algo salio mal')

def show_data():
   print(env.get('CLOUD_NAME'))
   print(env.get('API_KEY'))
   print(env.get('API_SECRET'))