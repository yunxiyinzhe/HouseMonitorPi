#coding=utf-8
import socket
import os
from widget_utils import getPiStatus
from serial_utils import serial_reslut
import threading

def run_pi_robot_server():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if os.path.exists('/tmp/pi_robot.d'):
        os.unlink('/tmp/pi_robot.d')
    sock.bind('/tmp/pi_robot.d')
    sock.listen(5)

    while True:
        print 'waiting for connection...'
        connection,address = sock.accept()

        while True:
            cmd = str(connection.recv(1024))
            if cmd == 'home':
                reply = 'The current temperature is ' + str(serial_reslut['tmp']) + \
                '°C, humidity is ' + str(serial_reslut['hum']) + \
                '%, PM2.5 is ' + str(serial_reslut['pm_2_5']) + \
                'μg/m³, PM10 is ' + str(serial_reslut['pm_10']) + \
                'μg/m³, formaldehyde concentration is ' + str(serial_reslut['CH2O']) + '/1000 mg/m3 .'
                connection.send(reply)
            elif cmd == 'pie':
                pie_status = getPiStatus()
                reply = 'The Raspberry status is: CPU usage:' + str(pie_status['cpu_usage']) + \
                'us, CPU temperature:' + str(pie_status['cpu_tmp']) + \
                '°C, Ram used:' + str(pie_status['ram_used']) + \
                'MB, Ram used percentage:' + str(pie_status['ram_percentage']) + \
                '%, Disk used:' + str(pie_status['disk_used']) + \
                'GB, Disk used percentage:' + str(pie_status['disk_percentage']) + '%.'
                connection.send(reply)
        connection.close()
    sock.close()

threading.Thread(target=run_pi_robot_server).start()
