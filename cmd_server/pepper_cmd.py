#!/usr/bin/env python

import time
import os
import socket
import math

session = None
tts_service = None
memory_service = None
motion_service = None

# Begin/end

def begin():
	global tts_service, memory_service, motion_service
	print 'begin'

	#Starting services
	memory_service  = session.service("ALMemory")
	motion_service  = session.service("ALMotion")
	tts_service = session.service("ALTextToSpeech")
	tts_service.setLanguage("Italian")


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

