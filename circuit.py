from config import *
import serial
import time


def get_temperature():
    # Leer el número enviado por el Arduino
    serial_port = serial.Serial("COM4", 9600, timeout=1)
    #time.sleep(2)
    while True:
        if serial_port.in_waiting > 0:
            line = serial_port.readline().decode("utf-8").strip()
            print(f"Data received from Arduino: {line}")
            return int(line)
    serial_port.close()


def set_temperature(serial_port, temperature):
    # Enviar un número al Arduino
    serial_port = serial.Serial("COM4", 9600, timeout=1)
    print(f"Sending data to Arduino: {temperature}")
    serial_port.write(f"{temperature}\n".encode("utf-8"))
    time.sleep(2)
    serial_port.close()

'''
def main():
    # Configurar la conexión serie
    serial_port = serial.Serial("COM6", 9600, timeout=1)
    time.sleep(2)  # Esperar a que la conexión se establezca

    try:
        while True:
            # Enviar un número al Arduino
            set_temperature(serial_port, temperature)
            # Leer el número enviado por el Arduino
            get_temperature(serial_port)
            time.sleep(2)  # Esperar antes de la siguiente interacción

    except KeyboardInterrupt:
        print("Programa terminado.")
    finally:
        serial_port.close()


if __name__ == "__main__":
    main()
'''
"""
Resources:
Do connection with Arduino: https://www.luisllamas.es/controlar-arduino-con-python-y-la-libreria-pyserial/
Use Bluetooth module: https://computointegrado.blogspot.com/2012/02/python-arduino-con-modulo-de-bluetooth.html
"""
