# Weather API for automated irrigation system for Assignment 1
# Chad Finch - 16151947
# Rob Harper -
# Glenn Roslee - 

import RPi.GPIO as GPIO
import urllib2
import json
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#This is just for testing purposes
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

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
print ("Current Temp:")
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

# This will output to the LEDS for testing - this will change once the moisture sensor and relay are in place
# which then output to the solenoid for water release.
# we will need to add in a timer which will close the solenoid when the timer expires.

if currentforecast == 'Clear':
	print ('clear')
	GPIO.output(18, GPIO.HIGH)
	time.sleep(1)
	print ("LED OFF")
	GPIO.output(18, GPIO.LOW)
if currentforecast == 'Rain':
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
