#!/usr/bin/env python

import time
import os
import socket


session = None

# Begin/end

def begin():
	print 'begin'

    #Starting services
    memory_service  = session.service("ALMemory")

	


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
	print 'Say ',strsay



	


