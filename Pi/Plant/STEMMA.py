from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw


def read() -> (float, float):
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    # read temperature from the temperature sensor
    # read moisture level through capacitive touch pad
    return ss.get_temp(), ss.moisture_read()
