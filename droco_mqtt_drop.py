#!/usr/bin/env python3
from urllib.parse import parse_qsl, urljoin, urlparse

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

SERVO_FREQ = 50
SERVO_MIN = 2.5
SERVO_MAX = 12.5

servo = GPIO.PWM(18, SERVO_FREQ)
servo.start(0)


from time import sleep
from gpiozero import LED
import os,sys

import paho.mqtt.client as paho

led = LED(11)


def angle_to_duty_cycle(angle):
    duty_cycle = SERVO_MIN + (angle / 180.0) * (SERVO_MAX - SERVO_MIN)
    return duty_cycle

def set_servo_angle(angle):
    duty_cycle = angle_to_duty_cycle(angle)
    servo.ChangeDutyCycle(duty_cycle)

def on_connect(self, mosq, obj, rc):
        self.subscribe("servo", 0)
    
def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if(msg.payload == "payone"):    
        print("Payload One")
        set_servo_angle(30)    
    elif(msg.payload == "paytwo"):    
        print("Payload Two")
        set_servo_angle(60)
    elif(msg.payload == "reset"):    
        print("Latch Reset")
        set_servo_angle(0)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

    
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))



mqttc = paho.Client()                        # object declaration
# Assign event callbacks
mqttc.on_message = on_message                          # called as callback
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe


#url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883')                  # pass broker addr e.g. "tcp://iot.eclipse.org"
#url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.hivemq.com:1883')
url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
url = urlparse(url_str)

mqttc.connect(url.hostname, url.port)

rc = 0
while True:
    while rc == 0:
        import time   
        rc = mqttc.loop()
        #time.sleep(0.5)
    print("rc: " + str(rc))