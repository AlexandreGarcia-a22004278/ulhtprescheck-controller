import sys
import serial
import json

# Conecta ao Arduino
try:
    ser = serial.Serial('COM3', 9600)
    # Leia a resposta do Arduino
    response = ser.readline().decode('utf-8').rstrip()
    # Guarda o UDID do Arduino na variável identifier
    identifier = response
except Exception as e:
    print("Não existe comunicação com o Arduino. Verifique as configurações. Porta: COM3 / Canal: 9600")
    print(e)
    input("Pressione Enter para terminar...")
    sys.exit()

# Loop principal
while True:
    # Verifica se há dados disponíveis no buffer de recepção do Arduino
    if ser.in_waiting > 0:
        # Lê uma linha de dados do Arduino e remove a nova linha
        data = ser.readline().decode('utf-8').rstrip()
        payload = {"identifier": identifier, "uid": data}
        print(json.dumps(payload))
        break
