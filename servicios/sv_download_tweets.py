# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------------------------------------------
# Archivo: sv_download_tweets.py
# Tarea: 2 Arquitecturas Micro Servicios.
# Autor(es): Gilberto Estrada, Erick Ibarra, Iseal Fraire & Victor Reveles
# Version: 1.0 Mayo 2017
# Descripción:
#
#   Este Archivo define el rol de un servicio. Sun función principal es descargar Tweets de un tema en 
#   especifico, proporcionando todos los detalles de los tweets descargados haciendo uso de la libreria tweepy,
#   asi mismo usando el mandejador de base de datos sqlite para guardar los tweets recuperados.
#   
#
#
#
#                              sv_download_tweets.py
# +-----------------------+-------------------------+------------------------+
# |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
# +-----------------------+-------------------------+------------------------+
# |                       |  - Ofrecer un JSON que  | - Utiliza el API de    |
# |    Procesador de      |    contenga información |   twitter              |
# |     comentarios       |    detallada de un      | - Utiliza base de datos|
# |					  	  |	   tweet con una        |   sqlite3.             |
# |                       |    busqueda especifica. | - Utiliza libreria     |
# |              		  |                         |   tweepy.              |
# +-----------------------+-------------------------+------------------------+
#

import tweepy
from tweepy import OAuthHandler
from unidecode import unidecode
import sqlite3
import os
import json
from flask import Flask, abort, render_template, request
app = Flask (__name__)


#Se creó una aplicacion desde dev.twitter.com y esto nos generó las siguientes llaves para
#poder utilizar la API de twitter.
CKEY = "MTe1aN2WYDmfXROJUKApfHWhz"
CSECRET = "2iMHDbW962bNL3KfKh2CeTMUddITzJ1I8GOIuhbDUw4wHLaRTF"
ATOKEN = "603859293-zHtm1UIhPh3McLjtvjojhw0s72rBJEDH3BUMSgfk"
ATOKENSECRET = "eh2LqJZQxH0WxU7EIL6HN91pmzfUecVwXwxi9k7S0rFO7"

#TWEET_TOPIC: Determinamos el tema del cual se van a realizar las busquedas de
# los tweets.


#Determinamos en que lenguaje se haran las busquedas.
LANGUAGE = 'en'
#Determinamos el número maximo de tweets que deseamos obtener.
LIMIT = 1000

@app.route("/api/v1/download", methods=['GET'])
def get_tweets():
    TWEET_TOPIC = request.args.get("t")

    if TWEET_TOPIC is not None:
        auth = OAuthHandler(CKEY, CSECRET)
        auth.set_access_token(ATOKEN, ATOKENSECRET)
        api = tweepy.API(auth)
        tweets = []

        #Con un ciclo obtenemos los tweets encontrados y los vamos guardando en
        #  un arreglo para despues manipular estos mismos.
        for tweet in tweepy.Cursor(api.search, q=TWEET_TOPIC, result_type='recent',
		    				       include_entities=True, lang=LANGUAGE).items(LIMIT):
            aux = { "id": tweet.id,
			        "tweet_text": unidecode(tweet.text.replace('"','')),
    		        "query": TWEET_TOPIC,
    		        "language": LANGUAGE
    		        }
            tweets.append(aux)

        #La función connect nos permite conectarnos a la base de datos en caso
        #  de que ya fuera creada, si no de lo contrario, se va a crear una
        # base de datos nueva.
        conn = sqlite3.connect('tweets.db')

        #La función cursor() creamos un objeto de tipo cursor para poder
        # ejecutar comandos SQL.
        c = conn.cursor()

        #Con el comando execute realizamos la creacion de la base de datos en
        # caso de que no existiera la tabla, si la tabla ya fue creada,
        # se ignora esta ejecucion. En la tabla se implementaron 3 campos:
        #     -ID: Se guarda el ID de el tweet obtenido.
        #     -tweet_text: Se guarda el contendio del tweet.
        #     -query: Se guarda el nombre de la serie o pelicula.
        c.execute('CREATE TABLE IF NOT EXISTS Tweets (id text PRIMARY KEY, tweet_text text, query text)')

        #Sólo se insertan los tweets que no se habían guardado previamente
        for tweet in tweets:
            try:
                c.execute('INSERT INTO Tweets VALUES (:id, :tweet_text, :query)',
                          tweet)
            except sqlite3.IntegrityError:
                pass

        #La función commit() nos permite guardar los cambios realizados en la
                # base de datos.
        conn.commit()

        '''
        # Revisa si los datos fueron insertados a la tabla de la base de datos
        for row in c.execute('SELECT * FROM Tweets'):
            print(row)
        '''

        #Con la función close() cerramos la conexión a la base de datos.
        conn.close()
    else:
        abort(400)


if __name__ == '__main__':
	# Se define el puerto del sistema operativo que utilizará el servicio
	port = int(os.environ.get('PORT', 8085))
	# Se habilita la opción de 'debug' para visualizar los errores
	app.debug = True
	# Se ejecuta el servicio definiendo el host '0.0.0.0' para que se pueda acceder desde cualquier IP
	app.run(host='0.0.0.0', port=port)
