# Weather API for automated irrigation system for Assignment 1
# Chad Finch - 16151947
# Rob Harper - 96066910
# Glenn Roslee - 11062008

import RPi.GPIO as GPIO
import urllib2
import json
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

moistSensor = 21
water = True
moisture = True

#This is just for testing purposes | Output
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

# INPUT
GPIO.setup(moistSensor, GPIO.IN)


def checkMoisture(moistSensor):
	if GPIO.input(moistSensor):
                print('No water detected')
                water = False
	else:
                print('Water Detected')
        return water
		
def receiveTemp():
    "get temperature from weather api"
    APIResponse = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=62b4ad0fc294f7c579fbf3d3a5b49fb6&q=Auckland')
    data = APIResponse.read()
    return data

currentWeather = receiveTemp()
w = json.loads(currentWeather)

# Current Temp
temp = float(w['list'][0]['main']['temp'])
temp = (temp - 273) #convert from kelvin to Farenheit
print ("Current Temp: ")
print (round(temp))

# Weather Forecast
def receiveForecast():
    " get forecast from api "
    APIResponse = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=62b4ad0fc294f7c579fbf3d3a5b49fb6&q=Auckland')
    data = APIResponse.read()
    return data

currentWeather = receiveForecast()
w = json.loads(currentWeather)

#LOW TEMP
temp = float(w['list'][0]['main']['temp_min'])
temp = (temp - 273)
print ("Daily Low: ")
print (round(temp))

#HIGH TEMP
temp = float(w['list'][0]['main']['temp_max'])
temp = (temp - 273)
print ("Daily High: ")
print (round(temp))

#RAINFALL?
currentforecast = w['list'][0]['weather'][0]['main']
print ("The weather is: ")
print (currentforecast)

moisture = checkMoisture(moistSensor)

# This will output to the LEDS for testing - this will change once the moisture sensor and relay are in place
# which then output to the solenoid for water release.
if currentforecast == 'Clear' and moisture == False:
		print ('Start Water Flow')
		#tested with an LED
		GPIO.output(24, GPIO.HIGH)
		#Keep out on for 60 seconds
		time.sleep(60)
		print ("Stop Water Flow")
		GPIO.output(24, GPIO.LOW)

if currentforecast == 'Rain' and moisture == False:
        print ('No water required')
        print ('Rain forecasted for today')
	GPIO.output(18, GPIO.HIGH)
	time.sleep(30)
	#exit program
	GPIO.output(18, GPIO.LOW)
	exit()

if currentForecast == 'Clear' and water == True:
        print ('No water required, sufficient moisture detected')
        GPIO.output(18, GPIO.HIGH)
        time.sleep(30)
        #exit program
        GPIO.output(18, GPIO.LOW)
        exit()
                

"""
print ('rain')
	GPIO.output(23, GPIO.HIGH)
	time.sleep(1)
	print ("LED OFF")
	GPIO.output(23, GPIO.LOW)
if currentforecast == 'Clouds':
	print ('clouds')
	GPIO.output(24, GPIO.HIGH)
	time.sleep(1)
	print ("LED OFF")
	GPIO.output(24, GPIO.LOW)
if currentforecast == 'Snow':
	print ('snow')
	GPIO.output(25, GPIO.HIGH)
	time.sleep(1)
	print ("LED OFF")
	GPIO.output(25, GPIO.LOW)
"""

