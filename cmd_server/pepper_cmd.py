#!/usr/bin/env python

import time
import os
import socket
import threading
import math
import random
import qi

app = None
session = None
tts_service = None
memory_service = None
motion_service = None
anspeech_service = None
tablet_service = None

robot = None        # PepperRobot object

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# Sensors
headTouch = 0.0
handTouch = [0.0, 0.0] # left, right
sonar = [0.0, 0.0] # front, back


# Sensors

def sensorThread(robot):
    sonarValues = ["Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value",
                  "Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"]
    headTouchValue = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
    handTouchValues = [ "Device/SubDeviceList/LHand/Touch/Back/Sensor/Value",
                   "Device/SubDeviceList/RHand/Touch/Back/Sensor/Value" ]

    t = threading.currentThread()
    while getattr(t, "do_run", True):
        robot.headTouch = robot.memory_service.getData(headTouchValue)
        robot.handTouch = robot.memory_service.getListData(handTouchValues)
        robot.sonar = robot.memory_service.getListData(sonarValues)
        #print "Head touch middle value=", robot.headTouch
        #print "Hand touch middle value=", robot.handTouch
        #print "Sonar [Front, Back]", robot.sonar
        time.sleep(1)
    #print "Exiting Thread"





def touchcb(value):
    print "value=",value

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    print touched_bodies


def sensorvalue(sensorname):
    global robot
    if (robot!=None):
        return robot.sensorvalue(sensorname)


def sensorvalue_OLD(sensorname):
    global sonar, headTouch, handTouch
    if (sensorname == 'frontsonar'):
        return sonar[0]
    elif (sensorname == 'rearsonar'):
        return sonar[1]
    elif (sensorname == 'headtouch'):
        return headTouch
    elif (sensorname == 'lefthandtouch'):
        return handTouch[0]
    elif (sensorname == 'righthandtouch'):
        return handTouch[1]


# Begin/end

def begin():
    global robot
    print 'begin'
    if (robot==None):
        robot=PepperRobot()
        robot.connect()

def end():
    print 'end'
    time.sleep(0.5) # make sure stuff ends


def begin_OLD():
    global session, tts_service, memory_service, motion_service, anspeech_service, tablet_service
    print 'begin'

    if session==None:
        return

    #Starting services
    memory_service  = session.service("ALMemory")
    motion_service  = session.service("ALMotion")
    tts_service = session.service("ALTextToSpeech")
    anspeech_service = session.service("ALAnimatedSpeech")
    tablet_service = session.service("ALTabletService")

    #print "ALAnimatedSpeech ", anspeech_service
    #tts_service.setLanguage("Italian")
    tts_service.setLanguage("English")

    touch_service = session.service("ALTouch")
    touchstatus = touch_service.getStatus()
    #print touchstatus
    touchsensorlist = touch_service.getSensorList()
    #print touchsensorlist

    anyTouch = memory_service.subscriber("TouchChanged")
    idAnyTouch = anyTouch.signal.connect(touchcb)

    # create a thead that monitors directly the signal
    appThread = threading.Thread(target = apprunThread, args = ())
    appThread.start()




# Robot motion

def stop():
    global robot
    if (robot==None):
        begin()
    robot.stop()

def forward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.forward(r)

def backward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.backward(r)

def left(r=1):
    global robot
    if (robot==None):
        begin()
    robot.left(r)

def right(r=1):
    global robot
    if (robot==None):
        begin()
    robot.right(r)



# OLD style commands

def stop_OLD():
    global motion_service,session
    print 'stop'
    motion_service.stopMove()
    beh_service = session.service("ALBehaviorManager")
    bns = beh_service.getRunningBehaviors()
    for b in bns:
        beh_service.stopBehavior(b)

def forward_OLD(r=1):
    global motion_service
    print 'forward',r
    #Move in its X direction
    x = r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def backward_OLD(r=1):
    global motion_service
    print 'backward',r
    x = -r * 0.5
    y = 0.0
    theta = 0.0
    motion_service.moveTo(x, y, theta) #blocking function

def left_OLD(r=1):
    global motion_service
    print 'left',r
    #Turn 90deg to the left
    x = 0.0
    y = 0.0
    theta = math.pi/2 * r
    print 'motion_service = ',motion_service
    motion_service.moveTo(x, y, theta) #blocking function

def right_OLD(r=1):
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
    global robot
    print 'Say ',strsay
    if (robot==None):
        begin()
    robot.say(strsay)

def asay(strsay):
    global robot
    print 'Animated Say ',strsay
    if (robot==None):
        begin()
    robot.asay(strsay)


# OLD-style speech functions

def say_OLD(strsay):
    global tts_service
    print 'Say ',strsay
    tts_service.say(strsay)


def asay_OLD(strsay):
    global tts_service, anspeech_service
    print 'Say ',strsay
    #tts_service.say(strsay)

    # set the local configuration
    #configuration = {"bodyLanguageMode":"contextual"}

    # say the text with the local configuration

    # http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
    vanim = ["animations/Stand/Gestures/Enthusiastic_4",
             "animations/Stand/Gestures/Enthusiastic_5",
            "animations/Stand/Gestures/Excited_1",
            "animations/Stand/Gestures/Explain_1" ]
    anim = random.choice(vanim)

    if ('hello' in strsay):
        anim = "animations/Stand/Gestures/Hey_1"
    
    anspeech_service.say("^start("+anim+") " + strsay+" ^wait("+anim+")")






# Other 

def stand():
	global session, tts_service
	print 'Stand'
	al_service = session.service("ALAutonomousLife")
	if al_service.getState()!='disabled':
		al_service.setState('disabled')
	rp_service = session.service("ALRobotPosture")
	rp_service.goToPosture("Stand",2.0)
	#tts_service.say("Standing up")


def disabled():
	global session, tts_service
	print 'Sleep'
	tts_service.say("Bye bye")
	al_service = session.service("ALAutonomousLife")
	al_service.setState('disabled')


def interact():
	global session, tts_service
	print 'Interactive mode'
	tts_service.say("Interactive")
	al_service = session.service("ALAutonomousLife")
	al_service.setState('interactive')


def run_behavior(bname):
	global session
	beh_service = session.service("ALBehaviorManager")
	beh_service.startBehavior(bname)
	#time.sleep(10)
	#beh_service.stopBehavior(bname)


def takephoto():
	global session, tts_service
	str = 'Take photo'
	print(str)
	#tts_service.say(str)
	bname = 'takepicture-61492b/behavior_1'
	run_behavior(bname)


def opendiag():
	global session, tts_service
	str = 'demo'
	print(str)
	bname = 'animated-say-5b866d/behavior_1'
	run_behavior(bname)

def sax():
	global session, tts_service
	str = 'demo'
	print(str)
	bname = 'saxophone-0635af/behavior_1'
	run_behavior(bname)



class PepperRobot:

    def __init__(self):
        self.isConnected = False
        # Sensors
        self.headTouch = 0.0
        self.handTouch = [0.0, 0.0] # left, right
        self.sonar = [0.0, 0.0] # front, back
        self.language = "English"

    # Connect to the robot
    def connect(self, pip=os.environ['PEPPER_IP'], pport=9559):

        if (self.isConnected):
            print("Robot already connnected.")
            return

        print("Connecting to robot %s:%d ..." %(pip,pport))
        try:
            connection_url = "tcp://" + pip + ":" + str(pport)
            self.app = qi.Application(["Pepper command", "--qi-url=" + connection_url ])
            self.app.start()
        except RuntimeError:
            print("%sCannot connect to Naoqi at %s:%d %s" %(RED,pip,pport,RESET))
            self.session = None
            return

        print("%sConnected to robot %s:%d %s" %(GREEN,pip,pport,RESET))
        self.session = self.app.session

        print("Starting services...")

        #Starting services
        self.memory_service  = self.session.service("ALMemory")
        self.motion_service  = self.session.service("ALMotion")
        self.tts_service = self.session.service("ALTextToSpeech")
        self.anspeech_service = self.session.service("ALAnimatedSpeech")
        self.tablet_service = self.session.service("ALTabletService")
        self.animation_player_service = self.session.service("ALAnimationPlayer")
        self.beh_service = self.session.service("ALBehaviorManager")
        self.al_service = self.session.service("ALAutonomousLife")
        self.rp_service = self.session.service("ALRobotPosture")

        webview = "http://198.18.0.1/apps/spqrel/index.html"
        self.tablet_service.showWebview(webview)

        self.touch_service = self.session.service("ALTouch")
        self.touchstatus = self.touch_service.getStatus()
        #print touchstatus
        self.touchsensorlist = self.touch_service.getSensorList()
        #print touchsensorlist

        #anyTouch = self.memory_service.subscriber("TouchChanged")
        #idAnyTouch = anyTouch.signal.connect(touchcb)

        # create a thead that monitors directly the signal
        sth = threading.Thread(target = sensorThread, args = (self, ))
        sth.start()

        self.isConnected = True


    # Speech sounds
    def setLanguage(self, language):
        self.tts_service.setLanguage(language)
    
    def say(self, interaction):
        self.tts_service.setParameter("speed", 80)
        self.tts_service.say(interaction)

    def asay(self, interaction):
        # set the local configuration
        #configuration = {"bodyLanguageMode":"contextual"}

        # http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
        vanim = ["animations/Stand/Gestures/Enthusiastic_4",
                 "animations/Stand/Gestures/Enthusiastic_5",
                 "animations/Stand/Gestures/Excited_1",
                 "animations/Stand/Gestures/Explain_1" ]
        anim = random.choice(vanim) # random animation

        if ('hello' in interaction):
            anim = "animations/Stand/Gestures/Hey_1"
    
        self.anspeech_service.say("^start("+anim+") " + interaction+" ^wait("+anim+")")



    def bip(self, r=1):
	    print 'bip -- NOT IMPLEMENTED'


    def bop(self, r=1):
	    print 'bop -- NOT IMPLEMENTED'


    def animation(self, interaction):
        print 'Animation ',interaction
        self.animation_player_service.run(interaction)


    # Tablet

    def showurl(self, weburl):
        strurl = "http://198.18.0.1/apps/spqrel/%s" %(weburl)
        print "URL: ",strurl
        self.tablet_service.showWebview(strurl)

    # Robot motion

    def stop(self):
        print 'stop'
        self.motion_service.stopMove()
        bns = self.beh_service.getRunningBehaviors()
        for b in bns:
            self.beh_service.stopBehavior(b)

    def forward(self, r=1):
        print 'forward',r
        #Move in its X direction
        x = r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def backward(self, r=1):
        global motion_service
        print 'backward',r
        x = -r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def left(self, r=1):
        print 'left',r
        #Turn 90deg to the left
        x = 0.0
        y = 0.0
        theta = math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    def right(self, r=1):
        global motion_service
        print 'right',r
        #Turn 90deg to the right
        x = 0.0
        y = 0.0
        theta = -math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    # Wait

    def wait(self, r=1):
	    print 'wait',r
	    for i in range(0,r):
		    time.sleep(3)

    # Sensors

    def sensorvalue(self, sensorname):
        if (sensorname == 'frontsonar'):
            return self.sonar[0]
        elif (sensorname == 'rearsonar'):
            return self.sonar[1]
        elif (sensorname == 'headtouch'):
            return self.headTouch
        elif (sensorname == 'lefthandtouch'):
            return self.handTouch[0]
        elif (sensorname == 'righthandtouch'):
            return self.handTouch[1]


    # Behaviors

    def stand(self):
        if self.al_service.getState()!='disabled':
            self.al_service.setState('disabled')
        self.rp_service.goToPosture("Stand",2.0)

    def disabled():
        #self.tts_service.say("Bye bye")
        self.al_service.setState('disabled')

    def interactive():
	    #tts_service.say("Interactive")
	    self.al_service.setState('interactive')


    def run_behavior(bname):
	    self.beh_service.startBehavior(bname)
	    #time.sleep(10)
	    #beh_service.stopBehavior(bname)

    def sax():
	    str = 'sax'
	    print(str)
	    bname = 'saxophone-0635af/behavior_1'
	    run_behavior(bname)

    def takephoto():
	    str = 'take photo'
	    print(str)
	    #tts_service.say("Cheers")
	    bname = 'takepicture-61492b/behavior_1'
	    run_behavior(bname)

    def introduction():
	    str = 'introduction'
	    print(str)
	    bname = 'animated-say-5b866d/behavior_1'
	    run_behavior(bname)


