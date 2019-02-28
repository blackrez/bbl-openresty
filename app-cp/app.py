from flask import Flask, jsonify, g, request

import redis

import mysql.connector
import mysql.connector.pooling

app = Flask(__name__)


app.r = redis.Redis(host='redis', port=6379, db=0)

dbconfig = {'user':"root", 'host':'mysql-codepostaux', 'database':"codepostaux"}
app.cnx_pool= mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
                              **dbconfig)


@app.route("/v1/code_postaux/", methods=['GET'])
def code_all():
    query = ("SELECT code_insee, nom_commune, code_postal FROM codepostaux;")
    conn = app.cnx_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = []
    for (code_insee, nom_commune, code_postal) in cursor:
        result.append({'code_insee': code_insee,
        'nom_commune': nom_commune.title(),
        'code_postal': code_postal})
    return jsonify({'result':result})

@app.route("/v1/code_postal/<cp>", methods=['GET'])
def code_single(cp):
    query = ("SELECT code_insee, nom_commune, code_postal FROM codepostaux WHERE code_postal = %s;")
    conn = app.cnx_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (cp,))
    result = []
    for (code_insee, nom_commune, code_postal) in cursor:
        result.append({'code_insee': code_insee,
        'nom_commune': nom_commune.title(),
        'code_postal': code_postal,})
    return jsonify({'result':result})

#@app.route("/v1/ville/search<str:cp>", methods=['GET'])
#def ville():
#    return jsonify({})

@app.route("/v1/code_postal/geosearch", methods=['GET'])
def geosearch():
    x = request.args.get('x')
    y = request.args.get('y')
    code_insee = app.r.georadius('Centroid', x, y, '10', 'km')
    com = []
    for ci in code_insee:
        nom_commune = app.r.hmget(ci, 'nom_commune')[0]
        code_postal = app.r.hmget(ci, 'code_postal')[0]
        com.append({'nom_commune': nom_commune.decode("utf-8") , 'code_postal': code_postal.decode("utf-8") })
    return jsonify({'result':com})


if __name__ == "__main__":
    app.debug = True
    app.run()