#!/usr/bin/env python

import time
import os
import socket


session = None
tts_service = None
memory_service = None


# Begin/end

def begin():
	global tts_service, memory_service
	print 'begin'

	#Starting services
	memory_service  = session.service("ALMemory")
	tts_service = session.service("ALTextToSpeech")
	tts_service.setLanguage("Italian")


def end():
	print 'end'
	time.sleep(0.5) # make sure stuff ends


# Robot motion

def stop():
	print 'stop'
	


def forward(r=1):
	print 'forward',r
	


def backward(r=1):
	print 'backward',r
	


def left(r=1):
	print 'left',r
	


def right(r=1):
	print 'right',r
	


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

