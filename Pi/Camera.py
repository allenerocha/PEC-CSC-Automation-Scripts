import base64
import datetime
from picamera import PiCamera
from time import time


class cam:
    def __init__(self, image_name: str, test_number: str) -> None:
        if type(test_number) != type(str) or type(image_name) != type(str):
            raise TypeError("image_name and test_number parameter must be of type str!")
        self.image_data = str()
        mon = datetime.datetime.now().strftime("%b")
        day = datetime.datetime.now().strftime("%d")
        year = datetime.datetime.now().strftime("%y")
        camera = PiCamera()
        camera.resolution = (3280, 2464)
        # example '/home/pi/data/Nov-27-19/plant-1.jpg
        camera.capture('/home/pi/data/{}-{}-{}/{}-{}.jpg'.format(mon, day, year, image_name, test_number))
        self.image_data = self.encode_image('/home/pi/data/{}-{}-{}/{}-{}.jpg'.format(mon, day, year, image_name, test_number))

    def encode_image(self, image_path: str) -> str:
        """
        :param image_path: full directory path to image
        :return: image as base64
        """
        if type(image_path) != type(str):
            raise TypeError('Image path must be of type str!')
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read())
