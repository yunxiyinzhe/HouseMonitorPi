import json
import os
from urllib import urlopen

def get_weather_outdoor():
    data = urlopen('https://free-api.heweather.com/v5/weather?city=shanghai&key=***********************').read()
    data_json = json.loads(data.decode('utf-8'))
    result = {'tmp': 'N/A', 'hum': 'N/A', 'aqi': 'N/A', 'wind': 'N/A'}
    if data_json['HeWeather5'][0]['status'] == 'ok':
        result['tmp'] = data_json['HeWeather5'][0]['now']['tmp'].encode('utf-8')
        result['hum'] = data_json['HeWeather5'][0]['now']['hum'].encode('utf-8')
        result['aqi'] = data_json['HeWeather5'][0]['aqi']['city']['aqi'].encode('utf-8')
        result['wind'] = data_json['HeWeather5'][0]['now']['wind']['spd'].encode('utf-8')
    return result

def getCPUtemperature():
    result = 0.0
    try:
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        res = tempFile.read()
        result=float(res)/1000
    except:
        print('can not open get CPU temperature')
    return result

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def getCPUuse():
    return(str(os.popen("top -bn2 | grep Cpu | head -n 2 | tail -n 1| awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def getPiStatus():
    result = {'cpu_usage': 0.0, 'cpu_tmp': 0.0,
              'ram_total': 0, 'ram_used': 0, 'ram_percentage': 0,
              'disk_total': '0.0', 'disk_used': '0.0','disk_percentage': 0}
    result['cpu_usage'] = float(getCPUuse().split('%')[0])
    result['cpu_tmp'] = getCPUtemperature()
    ram_stats = getRAMinfo()
    result['ram_total'] = int(ram_stats[0]) / 1024
    result['ram_used'] = int(ram_stats[1]) / 1024
    result['ram_percentage'] = int(result['ram_used']*100/result['ram_total'])
    disk_stats = getDiskSpace()
    result['disk_total'] = disk_stats[0]
    result['disk_used'] = disk_stats[1]
    result['disk_percentage'] = disk_stats[3].split('%')[0]
    return result
