import csv
import mysql.connector

# cnx = mysql.connector.connect(user="root", database="codepostaux")
cnx = mysql.connector.connect(user="root", host="mysql-codepostaux")
try:
    cursor = cnx.cursor()
except:
    cnx.reconnect(attempts=5, delay=5)
create_db = ("CREATE DATABASE IF NOT EXISTS codepostaux;"
            "USE codepostaux;")

cursor.execute(create_db)
add_cp  = ("INSERT INTO codepostaux" 
           "(code_insee, nom_commune, code_postal, libelle, ligne_5, centroid) " 
           "VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))") 


with open('/tmp/laposte_hexasmal.csv') as csvfile:    
    cpreader = csv.reader(csvfile, delimiter=";") 
    fitstline = True 
    for row in cpreader: 
        print(row) 
        if fitstline: 
            fitstline = False 
        else: 
            if row[5] == '': 
                row[5] = "POINT(0 0)" 
            else: 
                row[5] = "POINT({})".format(row[5].replace(',', ""))
            try:
                cursor.execute(add_cp, row)
            except:
                cnx.reconnect(attempts=5, delay=5)

cnx.commit()
cnx.close()