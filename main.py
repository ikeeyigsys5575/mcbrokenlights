import time
import requests
import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BCM)

url = "https://mcbroken.com/markers.json"


status = []



response = requests.get(url)

with open('config.json', 'r') as f:
    config = json.load(f)

targetAddresses = config['addresses']
gpioBroken = config['gpioBroken']
gpioGood = config['gpioWorking']

def refresh():
    if response.status_code == 200:
        status.clear()
        for address in targetAddresses:
            data = response.json();
            featuresArray = data['features']
            for feature in featuresArray:
                propertiesArray = feature['properties']
                if (propertiesArray['street'] == address):
                    status.append(propertiesArray['dot'])

    for gpio in gpioBroken:
        GPIO.setup(gpio, GPIO.OUT)

    for gpio in gpioGood:
        GPIO.setup(gpio, GPIO.OUT)

    for i in range(len(status)):
        if (status[i] == "broken"):
            GPIO.output(gpioBroken[i], GPIO.HIGH)
            GPIO.output(gpioGood[i], GPIO.LOW)
        elif (status[i] == "working"):
            GPIO.output(gpioBroken[i], GPIO.LOW)
            GPIO.output(gpioGood[i], GPIO.HIGH)
        else:
            GPIO.output(gpioBroken[i], GPIO.LOW)
            GPIO.output(gpioGood[i], GPIO.LOW)

    print(status)

while True:
    refresh()
    time.sleep(600)

GPIO.cleanup()

