#!/usr/bin/env python

import time
import os
import socket
import threading
import math
import qi

app = None
session = None
tts_service = None
memory_service = None
motion_service = None

# Sensors
headTouch = 0.0
sonarValues = [0,0] # front, back

# Connect to the robot
def robotconnect(pip=os.environ['PEPPER_IP'], pport=9559):
    global app, session
    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Pepper command", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n")
        session = None
        return        
    app.start()
    session = app.session
    begin()


def apprunThread():
    global memory_service, headTouch, sonarValues
    #app.run()
    sonarValueList = ["Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value",
                  "Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"]
    hmMemoryDataValue = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        headTouch = memory_service.getData(hmMemoryDataValue)
        sonarValues = memory_service.getListData(sonarValueList)
        #print "Head touch middle value=", headTouch
        #print "Sonar [Front, Back]", sonarValues
        time.sleep(1)
    #print "Exiting Thread"



# Sensors

def touchcb(value):
    print "value=",value

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    print touched_bodies



# Begin/end

def begin():
    global session, tts_service, memory_service, motion_service
    print 'begin'

    #Starting services
    memory_service  = session.service("ALMemory")
    motion_service  = session.service("ALMotion")
    tts_service = session.service("ALTextToSpeech")
    #tts_service.setLanguage("Italian")
    tts_service.setLanguage("English")

    touch_service = session.service("ALTouch")
    touchstatus = touch_service.getStatus()
    print touchstatus
    touchsensorlist = touch_service.getSensorList()
    print touchsensorlist

    anyTouch = memory_service.subscriber("TouchChanged")
    idAnyTouch = anyTouch.signal.connect(touchcb)

    #create a thead that monitors directly the signal
    appThread = threading.Thread(target = apprunThread, args = ())
    appThread.start()



def end():
    print 'end'
    time.sleep(0.5) # make sure stuff ends


# Robot motion

def stop():
	print 'stop'
	


def forward(r=1):
    global motion_service
    print 'forward',r
    #Move in its X direction
    x = r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def backward(r=1):
    global motion_service
    print 'backward',r
    x = -r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def left(r=1):
    global motion_service
    print 'left',r
    #Turn 90deg to the left
    x = 0.0
    y = 0.0
    theta = math.pi/2 * r
    print 'motion_service = ',motion_service
    motion_service.moveTo(x, y, theta) #blocking function

def right(r=1):
    global motion_service
    print 'right',r
    #Turn 90deg to the right
    x = 0.0
    y = 0.0
    theta = -math.pi/2 * r
    motion_service.moveTo(x, y, theta) #blocking function
	


# Wait

def wait(r=1):
	print 'wait',r
	for i in range(0,r):
		time.sleep(3)


# Sounds

def bip(r=1):
	print 'bip'


def bop(r=1):
	print 'bop'

# Speech

def say(strsay):
	global tts_service
	print 'Say ',strsay
	tts_service.say(strsay)



