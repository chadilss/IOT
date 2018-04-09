# Weather API for automated irrigation system for Assignment 1
# Chad Finch - 16151947
# Rob Harper - 96066910
# Glenn Roslee - 11062008

import RPi.GPIO as GPIO
import urllib2
import json
import time
import os
import subprocess


# Libraries for email notification
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

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

#Check Network Connection
hostname = "www.openweathermap.org"
response = os.system("ping -c 1 " + hostname + " > /Home/pi/IOT 2>&1")

#Check Response
if response == 0:
	print hostname, 'is up'
else:
	print hostname, 'is down'

# INPUT
GPIO.setup(moistSensor, GPIO.IN)

def sendEmail(msg):
	username = "waterworksnotification@gmail.com"
	password = "waterworks2018"
	# Group 18 members
	mailto = "chadfinch85@gmail.com"
	
	msg['From'] = username
	msg['To'] = mailto
	
	# Email comes from waterworksnotification@gmail.com
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username, password)
	server.sendmail(username, mailto, msg.as_string())
	server.quit()
	
	print "Email sent to: "+ mailto
	return

def water_started_email():
	print "Water Flow started"
	msg = MIMEMultipart()
	msg.attach(MIMEText('System Activated, Running for 1 Min. Water on'))
	msg['Subject'] = 'Watering System Notification'
	sendEmail(msg)
	return

def water_stopped_email():
	print "Water Flow Stopped"
	msg = MIMEMultipart()
	msg.attach(MIMEText('System Cycle Completed, water off'))
	msg['Subject'] = 'Watering System Notification'
	sendEmail(msg)
	return

def water_not_required_email():
	print "Water Not required"
	msg = MIMEMultipart()
	msg.attach(MIMEText('No water required today, rain or sufficient moisture detected'))
	msg['Subject'] = 'Watering System Notification'
	sendEmail(msg)
	return

def api_offline_email():
	print "API Error"
	msg = MIMEMultipart()
	msg.attach(MIMEText('WaterWorks irrigation is unable to contact the weather API'))
	msg['Subject'] = 'Watering System Notification'
	sendEmail(msg)
	return

def checkMoisture(moistSensor):
	if GPIO.input(moistSensor):
                print('No water detected')
                water = False
	else:
                print('Water Detected')
		water = True
        return water
		
def receiveTemp():
    "get temperature from weather api"
    APIResponse = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=62b4ad0fc294f7c579fbf3d3a5b49fb6&q=Auckland')
    data = APIResponse.read()
    return data

try:
	currentWeather = receiveTemp()
	w = json.loads(currentWeather)
except:
	api_offline_email()
	exit()

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
		water_started_email()
		#tested with an LED
		GPIO.output(24, GPIO.HIGH)
		#Keep out on for 60 seconds
		time.sleep(60)
		print ("Stop Water Flow")
		GPIO.output(24, GPIO.LOW)
		water_stopped_email()

if currentforecast == 'Rain' and moisture == False:
        print ('No water required')
        print ('Rain forecasted for today')
	water_not_required_email()
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

