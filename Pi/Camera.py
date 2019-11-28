import base64
import datetime
from picamera import PiCamera


def encode_image(image_name: str, test_number: str) -> str:
    if type(test_number) != type(str) or type(image_name) != type(str):
        raise TypeError("image_name and test_number parameter must be of type str!")
    mon = datetime.datetime.now().strftime("%b")
    day = datetime.datetime.now().strftime("%d")
    year = datetime.datetime.now().strftime("%y")
    path = '/home/pi/data/{}-{}-{}/{}-{}.jpg'.format(mon, day, year, image_name, test_number)
    camera = PiCamera()
    camera.resolution = (3280, 2464)
    # example '/home/pi/data/Nov-27-19/plant-1.jpg
    camera.capture(path)

    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read())

