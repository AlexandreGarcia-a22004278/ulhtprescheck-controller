import os
import sys
import json
import serial
import requests
import jwt
from dotenv import load_dotenv

load_dotenv('.flaskenv')


def connect_to_arduino(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate)
        response = ser.readline().decode('utf-8').rstrip()
        identifier = 'ULHT-A-F23'  # TODO: Mudar para o identificador do Arduino 'response'
        return ser, identifier
    except Exception as e:
        print(json.dumps({
            "error": True,
            "message": f"Não existe comunicação com o Arduino. Verifique as configurações. Porta: {port} / Canal: {baud_rate}"
        }))
        return None, None


def read_data_from_arduino(ser):
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        return data
    else:
        return None


def send_data(backend_url, tipo, identifier, data):
    match tipo:
        case 'registo':
            print(json.dumps({"identifier": identifier, "uid": data, "error": False}))
            sys.exit()

        case 'aula':
            print(json.dumps({"identifier": identifier, "uid": data, "error": False}))
            token = jwt.encode(payload={"identifier": identifier, "uid": data},
                               key=os.environ.get('SECRET_KEY'),
                               algorithm='HS256')
            try:
                sent_data = requests.put(f"{backend_url}/presencas/arduino", json={'token': token})
                print(sent_data.status_code, sent_data.text)
                sent_data.close()
            except ConnectionError:
                print(json.dumps({
                    "error": True,
                    "message": f"Não existe comunicação com o backend. Verifique as configurações. URL: {backend_url}"
                }))

        case _:
            sys.exit()


def main():
    port = 'COM3'
    baud_rate = 9600
    tipo = sys.argv[1]
    backend_url = 'http://localhost:5000'

    ser, identifier = connect_to_arduino(port, baud_rate)
    if not ser or not identifier:
        sys.exit()

    while True:
        data = read_data_from_arduino(ser)

        if data is None:
            continue

        send_data(backend_url, tipo, identifier, data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit()
    finally:
        sys.exit()
