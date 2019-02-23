import csv
import mysql.connector

cnx = mysql.connector.connect(user="brian", database="codepostaux", password="nice_try haxx0rs")
cursor = cnx.cursor()

add_cp  = ("INSERT INTO codepostaux" 
           "(code_insee, nom_commune, code_postal, libelle, ligne_5, centroid) " 
           "VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))") 


with open('/tmp/data/laposte_hexasmal.csv') as csvfile:    
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
            cursor.execute(add_cp, row)

cnx.commit()
cnx.close()