import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="mysqlpass",
                           db="urlsApp")

    c = conn.cursor()
    return c, conn