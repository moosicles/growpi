import Adafruit_DHT


def water_content(data_pin):
    pass


def temp_hum(sensor_model:string='2302', data_pin:int=4, farenheit=True):
    
    sensors = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    attempt = 0
    while attempt < 3:
        humidity, temperature = Adafruit_DHT.read_retry(sensors[sensor_model], data_pin)
        if humidity and temperature:
            if farenheit:
                temperature = temperature * 9/5.0 + 32
            return round(temperature, 2), round(humidity, 2)
    return 0, 0