from gpiozero import CPUTemperature

import sys
import time
import requests

API_THINGSPEAK_HOST = 'https://api.thingspeak.com/update'
THINGSPEAK_WRITE_KEY = '' # put your key here
MESUREMENT_INTERVAL = 300
DELAY = 30


def do_temp(field=0):
    try:
        cpu = CPUTemperature()

        t = cpu.temperature
    except OSError as err:
        t = 0

    print('temperature = %.2f' % t)

    global THINGSPEAK_WRITE_KEY

    if not THINGSPEAK_WRITE_KEY:
        print('not ThingSpeak key specified, skip sending data')
        return

    print('send data to ThingSpeak')

    data = '{"field%s":"%.2f"}' % (field, t)

    headers = {'X-THINGSPEAKAPIKEY': THINGSPEAK_WRITE_KEY,
               'Content-type': 'application/json'}

    r = requests.post(API_THINGSPEAK_HOST, data=data, headers=headers)
    results = r.json()

    print(results)

last_mesurement_time = 0
field = str(sys.argv[1])

while True:
    current_time = time.time()

    if current_time - last_mesurement_time > MESUREMENT_INTERVAL:
        do_temp(field)
        last_mesurement_time = current_time

    time.sleep(DELAY)
