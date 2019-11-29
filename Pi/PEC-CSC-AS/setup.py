from setuptools import find_packages, setup
# Required dependencies

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

required = [
    # Please keep alphabetized
    'adafruit_bme680',
    'base64',
    'board',
    'busio',
    'datetime',
    'json',
    'logging',
    'picamera'
]

setup(
    name='sensor_read',
    version='1.0',
    description="Gather data from sensors hooked up to the raspberry pi.",
    long_description=readme + '\n\n' + history,
    author="Allen Rocha",
    author_email='allenerocha@pm.me',
    url='https://github.com/allenerocha/PEC-CSC-Automation-Scripts',
    packages={'Pi.Plant': 'Plant', 'Pi.Outside': 'Outside'},
    include_package_data=True,
    install_requires=required,
    setup_requires=[
        'setuptools_scm >= 1.7.0'
    ],
    test_suite='tests',
    tests_require='unittest'
)
