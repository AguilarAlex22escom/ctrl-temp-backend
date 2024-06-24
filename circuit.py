from settings import *
import serial
import time

serial_port = serial.Serial("COM4", 9600, timeout=1)


def get_pressure():
    # Leer el número enviado por el Arduino
    # time.sleep(2)
    while True:
        if serial_port.in_waiting > 0:
            line = serial_port.readline().decode("utf-8").strip()
            print(f"Data received from Arduino: {line}")
            return int(line)


def set_pressure(serial_port, pressure):
    # Enviar un número al Arduino
    print(f"Sending data to Arduino: {pressure}")
    serial_port.write(f"{pressure}\n".encode("utf-8"))
    time.sleep(2)


def close_communication():
    serial_port.close()


"""
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
"""
"""
Resources:
Do connection with Arduino: https://www.luisllamas.es/controlar-arduino-con-python-y-la-libreria-pyserial/
Use Bluetooth module: https://computointegrado.blogspot.com/2012/02/python-arduino-con-modulo-de-bluetooth.html
"""
