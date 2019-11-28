import board
import busio
import adafruit_bme680


def read() -> (float, float, int, float):
    """
    :return: (temperature, humidity, gas, pressure)
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    return sensor.temperature, sensor.humidity, sensor.gas, sensor.pressure
