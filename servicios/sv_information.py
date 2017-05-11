# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: sv_information.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.0 Abril 2017
# Descripción:
#
#   Este archivo define el rol de un servicio. Su función general es porporcionar en un objeto JSON
#   información detallada acerca de una pelicula o una serie en particular haciendo uso del API proporcionada
#   por IMDb ('https://www.imdb.com/').
#   
#   
#
#                              sv_information.py
# +-----------------------+-------------------------+------------------------+
# |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
# +-----------------------+-------------------------+------------------------+
# |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
# |    Procesador de      |    contenga información |   IMDb.                |
# |     comentarios       |    detallada de pelí-   | - Devuelve un JSON con |
# |       de IMDb         |    culas o series en    |   datos de la serie o  |
# |                       |    particular.          |   pelicula en cuestión.|
# +-----------------------+-------------------------+------------------------+
#
#	Ejemplo de uso: Abrir navegador e ingresar a http://localhost:8084/api/v1/information?t=matrix
#
import os
from flask import Flask, abort, render_template, request
import urllib, json
app = Flask (__name__)

@app.route("/api/v1/information")
def get_information():
	# Método que obtiene la información de IMDB acerca de un título en particular
	# Se lee el parámetro 't' que contiene el título de la película o serie que se va a consultar
	title = request.args.get("t")
	# Se verifica si el parámetro no esta vacío 
	if title is not None:
		# Se conecta con el servicio de IMDb a través de su API
		url_omdb = urllib.urlopen("http://www.omdbapi.com/?t="+title+"&plot=full&r=json")
		# Se lee la respuesta de IMDb
		json_omdb = url_omdb.read()
		# Se convierte en un JSON la respuesta recibida
		omdb = json.loads(json_omdb)
		# Se regresa el JSON de la respuesta
		return json.dumps(omdb)
	else:
		# Se devuelve un error 400 para indicar que el servicio no puede funcionar sin parámetro
		abort(400)

if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el servicio
	port = int(os.environ.get('PORT', 8084))
	# Se habilita la opción de 'debug' para visualizar los errores
	app.debug = True
	# Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
	app.run(host='0.0.0.0', port=port)
