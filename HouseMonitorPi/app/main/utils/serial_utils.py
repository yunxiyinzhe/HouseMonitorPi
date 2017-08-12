import serial
from time import sleep
from threading import Timer

global ser
flag = False

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    flag = True
except:
    print('can not open ttyUSB0')

serial_reslut = {'status': 'uninitialized', 'tmp': 0.0, 'hum': 0.0, 'pm_2_5': 0, 'pm_10': 0, 'CH2O': 0}

def recvData():
    global ser
    global serial_reslut
    flag = False
    try:
        while True:
            data =ser.readall().split('\r\n')
            i = 0
            for value in data:
                if value == '#':
                    break
                else:
                    i = i + 1

            if (len(data) - i) > 6:
                if data[i + 6] == '*':
                    flag = True
                    serial_reslut['hum'] = data[i + 1]
                    serial_reslut['tmp'] = data[i + 2]
                    serial_reslut['pm_2_5'] = data[i + 3]
                    serial_reslut['pm_10'] = data[i + 4]
                    serial_reslut['CH2O'] = data[i + 5]
                    serial_reslut['status'] = 'initialized'
            if flag:
                f=open('tmp','wb')
                f.write(str(serial_reslut['hum'] + ' ' +
                        serial_reslut['tmp'] + ' ' +
                        serial_reslut['pm_2_5'] + ' ' +
                        serial_reslut['pm_10'] + ' ' +
                        serial_reslut['CH2O'] + ' ' +
                        serial_reslut['status']))
                break
    except:
        ser.close()
    t = Timer(5, recvData)
    t.start()

def get_serial_reslut():
    global serial_reslut
    reslut = {'status': serial_reslut['status'],
              'tmp': serial_reslut['tmp'],
              'hum': serial_reslut['hum'],
              'pm_2_5': serial_reslut['pm_2_5'],
              'pm_10': serial_reslut['pm_10'],
              'CH2O': serial_reslut['CH2O']}
    return reslut

if flag:
    recvData()