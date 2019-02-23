import json

import redis
import mysql.connector

cnx = mysql.connector.connect(user="brian", database="codepostaux", password="nice_try haxx0rs")
cursor = cnx.cursor()

r = redis.Redis(host='localhost', port=6379, db=0)

INDEX = 'Centroid'

if __name__ == '__main__':

    query = "SELECT nom_commune, code_postal, code_insee, ST_AsGeojson(centroid) FROM codepostaux"
    cursor.execute(query)
    for (nom_commune, code_postal, code_insee, geojson_raw) in cursor:

        geojson = json.loads(geojson_raw)
        print(geojson)
        print(code_insee)
        r.geoadd(INDEX, geojson['coordinates'][0], geojson['coordinates'][1], code_insee)
        r.hmset(code_insee, {"code_postal":code_postal, "nom_commune":nom_commune})
