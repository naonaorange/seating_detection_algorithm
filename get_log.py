import serial
import serial.tools.list_ports

LOG_PATH = './log.csv'
CATEGORY_NO = 1

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

    with serial.Serial(use_port) as ser:
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 5

        with open(LOG_PATH, mode='w') as f:
            try:
                while(True):
                    f.write(str(CATEGORY_NO) + ',')
                    for i in range(100):
                        data = ser.readline()
                        rssi = data.strip().decode('utf-8')    #バイト型を文字列変数に変換
                        rssi = int(rssi) * -1
                        print(rssi)
                        f.write(str(rssi) + ',')
                    f.write('\n')

            except Exception as e:
                print(e.message)
                pass