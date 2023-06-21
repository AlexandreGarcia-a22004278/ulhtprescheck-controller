import json
import os
import subprocess

import jwt
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})


@app.route('/arduino', methods=['GET'])
def arduino_leitor():
    try:
        output = subprocess.check_output(
            ['python', os.path.join(os.path.dirname(__file__), 'leitor.py')],
            stderr=subprocess.STDOUT,
            timeout=20,
            shell=True,
            input=None,
        )
        token = jwt.encode(payload=json.loads(output.decode("utf-8")),
                           key=app.config['SECRET_KEY'],
                           algorithm='HS256')

        return jsonify(token=token), 200
    except Exception as e:
        print(str(e))
        return 'Ocorreu um problema na leitura do arduino', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
