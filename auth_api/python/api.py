from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted

app = Flask(__name__)
login = Token()
protected = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST', 'GET'])
def url_login():
    username = request.args.get('username')
    password = request.args.get('password')
    res = {
        "data": login.generate_token(username, password)
    }
    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected", methods=['GET', 'POST'])
def url_protected():
    auth_token = request.headers.get('Authorization')
    res = {
        "data": protected.access_data(auth_token[7:])
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
