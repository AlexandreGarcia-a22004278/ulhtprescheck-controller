import json
import os
import subprocess

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['BACKEND_URL'] = os.environ.get('BACKEND_URL')
CORS(app, resources={r"/*": {"origins": app.config['BACKEND_URL']}})


@app.before_request
def check_auth():
    if not request.headers.get('Authorization'):
        return jsonify(error='Não autorizado'), 401

    try:
        token = request.headers.get('Authorization').split(' ')[1]
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

        if payload['identifier'] != os.environ.get('BACKEND_AUTH_TOKEN'):
            return jsonify(error='Não autorizado'), 401

    except jwt.ExpiredSignatureError:
        return jsonify(error='Token expirado'), 401
    except jwt.InvalidTokenError:
        return jsonify(error='Token inválido'), 401


@app.route('/arduino/<string:tipo>', methods=['GET'])
def arduino_leitor(tipo):
    try:
        match tipo:
            case 'aula':
                subprocess.run(['python', os.path.join(os.path.dirname(__file__), 'leitor.py'), 'aula'],
                               stderr=subprocess.STDOUT,
                               timeout=20,
                               shell=True,
                               input=None)
                return jsonify(message='Leitura iniciada'), 200

            case 'registo':
                output = subprocess.check_output(
                    ['python', os.path.join(os.path.dirname(__file__), 'leitor.py'), 'registo'],
                    stderr=subprocess.STDOUT,
                    timeout=20,
                    shell=True,
                    input=None,
                )

                json_data = json.loads(output.decode("utf-8"))

                if json_data['error']:
                    raise Exception(json_data['message'])

                token = jwt.encode(payload=json_data,
                                   key=app.config['SECRET_KEY'],
                                   algorithm='HS256')

                return jsonify(token=token), 200

            case _:
                raise Exception('Tipo de leitura não suportado')

    except Exception as e:
        print(str(e))
        return jsonify(error='Ocorreu um problema na leitura do arduino'), 500


@app.route('/arduino/encerrar', methods=['GET'])
def arduino_encerrar():
    try:
        os.system(f"pkill -f {os.path.join(os.path.dirname(__file__), 'leitor.py')}")
        return jsonify(message='Leitura do arduino encerrada'), 200
    except Exception as e:
        print(str(e))
        return jsonify(error='Ocorreu um problema ao encerrar a leitura do arduino'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
