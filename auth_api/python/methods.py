import mysql.connector
import jwt
import hashlib
from flask import abort

ENDPOINT = "sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com"
PORT = "3306"
USER = "secret"
REGION = "us-east-1"
DBNAME = "bootcamp_tht"
SECRET_KEY = "my2w7wjd7yXF64FIADfJxNs1oupTGAuW"


try:
    conn = mysql.connector.connect(
        host=ENDPOINT, user=USER, passwd="jOdznoyH6swQB9sTGdLUeeSrtejWkcw", port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
except Exception as e:
    print("Database connection failed due to {}".format(e))
    
class Token:

    def generate_token(self, username, password):
        cursor = conn.cursor()
        select_stmnt = "SELECT * FROM users where username = %(user)s"
        cursor.execute(select_stmnt, {'user': username})
        token_data = cursor.fetchone()
        if len(token_data) > 0:
            verify_hashh = password + token_data[2]
            hash_token = hashlib.sha512(verify_hashh.encode('utf-8')).hexdigest()
            if hash_token == token_data[1]:
                return jwt.encode({'role': token_data[3]}, SECRET_KEY)
        abort(403)

class Restricted:

    def access_data(self, authorization):
        decoded_token = jwt.decode(authorization, SECRET_KEY, algorithms=['HS256'])
        cursor = conn.cursor()
        select_stmnt = "SELECT role FROM users where role = %(role1)s"
        cursor.execute(select_stmnt, {'role1': decoded_token['role']})
        role_token = cursor.fetchone()
        if role_token:
            return "You are under protected data"
        abort(403)
