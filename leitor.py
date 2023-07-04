import sys
import json
import serial


def connect_to_arduino(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate)
        response = ser.readline().decode('utf-8').rstrip()
        identifier = '123'  # TODO: Mudar para o identificador do Arduino
        return ser, identifier
    except Exception as e:
        print("Não existe comunicação com o Arduino. Verifique as configurações. Porta: {} / Canal: {}".format(port,
                                                                                                               baud_rate))
        print(e)
        input("Pressione Enter para terminar...")
        sys.exit()


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

    while True:
        data = read_data_from_arduino(ser)
        if data is not None:
            payload = {"identifier": identifier, "uid": data}
            print(json.dumps(payload))
            break


if __name__ == "__main__":
    main()
