import sys
import json
import serial


def connect_to_arduino(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate)
        response = ser.readline().decode('utf-8').rstrip()
        identifier = '123'  # TODO: Mudar para o identificador do Arduino 'response'
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


def main():
    port = 'COM3'
    baud_rate = 9600

    ser, identifier = connect_to_arduino(port, baud_rate)

    if not ser or not identifier:
        sys.exit()

    while True:
        data = read_data_from_arduino(ser)
        if data is not None:
            print(json.dumps({"identifier": identifier, "uid": data, "error": False}))
            break


if __name__ == "__main__":
    main()
