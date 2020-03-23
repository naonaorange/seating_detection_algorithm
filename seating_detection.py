import serial
import serial.tools.list_ports
import numpy as np

import tensorflow as tf
from tensorflow.keras import models


def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[0]
    print('Use COM port: ' + use_port)

    return use_port

if __name__ == '__main__':

    use_port = search_com_port()
    model = models.load_model('model/seating_detection_algorithm.h5')

    with serial.Serial(use_port) as ser:
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 5

        try:
            while(True):
                rssi = []
                for i in range(100):
                    data = ser.readline()
                    r = data.strip().decode('utf-8')    #バイト型を文字列変数に変換
                    r = int(r) * -1
                    rssi.append(r)

                rssi = np.array(rssi, dtype=float)
                rssi = rssi.reshape(1,100)
                rssi = rssi * (-1) / 128
                #print(rssi)
                result = model.predict(rssi)
                print(result)

        except Exception as e:
            print(e.message)
            pass