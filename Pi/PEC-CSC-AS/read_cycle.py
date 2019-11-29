#!/usr/bin/env python3
from Pi.Outside import BME680
from Pi.Plant import STEMMA
from sys import argv
import Pi.Outside.Camera as cam
import time
import datetime
import logging
import json


def main(delay_sec: int) -> None:
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    """
    This function makes the calls to read the data from the sensors,
    then writes to a json file after waiting a certain amount of time
    :return:
    """
    try:
        delay = int(delay_sec)
    except ValueError as ev:
        print('Input value must be an integer!')
        logging.critical('{}\nFATAL ERROR WHILE PARSING VALUED ENTERED: {} TO INTEGER VALUE.'.format(ev, delay))

    while True:
        data = dict()
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        data['time'] = "{}:{}".format(hour, minute)
        stemma_temp, stemma_moisture = STEMMA.read()
        data['plant'] = [{"temperature": stemma_temp, "moisture": stemma_moisture,
                          "plant_img64": cam.encode_image('plant', str(format(datetime.datetime.now("%H"))))}]
        bme680_temperature, bme680_humidity, bme680_gas, bme680_pressure = BME680.read()
        data['outside'] = [{"temperature": bme680_temperature, "humidity": bme680_humidity, "pressure": bme680_pressure,
                            "gas": bme680_gas,
                            "outside_img64": cam.encode_image('plant', str(format(datetime.datetime.now("%H"))))}]
        mon = datetime.datetime.now().strftime("%b")
        day = datetime.datetime.now().strftime("%d")
        year = datetime.datetime.now().strftime("%y")
        path = '/home/pi/data/{}-{}-{}/data-{}-{}.json'.format(mon, day, year, hour, minute)
        with open(path, 'w') as json_file:
            json.dump(data, json_file)
        time.sleep(delay)


if __name__ == '__main__':
    main(argv[1])
