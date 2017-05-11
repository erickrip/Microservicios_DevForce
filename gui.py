# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: gui.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 1.2 Abril 2017
# Descripción:
#
#   Este archivo define la interfaz gráfica del usuario. Recibe dos parámetros que posteriormente son enviados
#   a servicios que la interfaz utiliza.
#   
#   
#
#                                   gui.py
# +-----------------------+-------------------------+------------------------+
# |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
# +-----------------------+-------------------------+------------------------+
# |                       |  - Porporcionar la in-  | - Consume servicios    |
# |          GUI          |    terfaz gráfica con la|   para proporcionar    |
# |                       |    que el usuario hará  |   información al       |
# |                       |    uso del sistema.     |   usuario.             |
# +-----------------------+-------------------------+------------------------+
#
import os
from flask import Flask, render_template, request
import urllib, json
import requests

app = Flask (__name__)

@app.route("/")
def index():
    # Método que muestra el index del GUI
    return render_template("index.html")

@app.route("/information", methods=['GET'])
def sentiment_analysis():
    # Se obtienen los parámetros que nos permitirán realizar la consulta
    title = request.args.get("t")
    url_omdb = urllib.urlopen("http://0.0.0.0:8084/api/v1/information?t="+title)
    # Se lee la respuesta de OMDB
    json_omdb = url_omdb.read()
    # Se convierte en un JSON la respuesta leída
    omdb = json.loads(json_omdb)

    # Se descargan los tweets y se guardan en la base de datos
    # No se asigna a ninguna variable ya que este microservicio no devuelve nada
    urllib.urlopen("http://0.0.0.0:8085/api/v1/download?t=" + title)

    # Obtiene los tweets previamente guardados en la base de datos
    url_stmt_analysis = urllib.urlopen("http://0.0.0.0:8086/api/v1/analysis?t="+title)
    # Se obtiene el JSON con la polaridad de todos los comentarios clasificados
    # Siempre y cuando la columna "query" de los registros en la base de
    # datos sea igual al parámetro "title" recibido de la GUI
    json_stmt_analysis = url_stmt_analysis.read()
    # Se convierte la respuesta leída en un JSON
    stmt_analysis = json.loads(json_stmt_analysis)


    # Se llena el JSON que se enviará a la interfaz gráfica para mostrársela al usuario
    json_result = {}

    json_result['pos_tweets'] = int(stmt_analysis['pos'])
    json_result['neg_tweets'] = int(stmt_analysis['neg'])
    json_result['ntl_tweets'] = int(stmt_analysis['ntl'])
    json_result['total_tweets'] = int(stmt_analysis['total'])
    json_result['omdb'] = omdb

    # Se regresa el template de la interfaz gráfica predefinido así como los datos que deberá cargar
    return render_template("status.html", result=json_result)


if __name__ == '__main__':
    # Se define el puerto del sistema operativo que utilizará el Sistema de Procesamiento de Comentarios (SPC).
    port = int(os.environ.get('PORT', 8000))
    # Se habilita el modo debug para visualizar errores
    app.debug = True
    # Se ejecuta el GUI con un host definido cómo '0.0.0.0' para que pueda ser accedido desde cualquier IP
    app.run(host='0.0.0.0', port=port)
