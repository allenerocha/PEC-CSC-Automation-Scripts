from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw


def read() -> float:
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
    # read moisture level through capacitive touch pad
    return ss.moisture_read()

