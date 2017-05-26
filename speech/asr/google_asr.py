import os
import requests
import urllib
import requests
import json
import sys
import tempfile
import time
from google.client import ASRClient

class GoogleASR:

	recognizing = False
	google_client = None
	audio_recorder = None
	leds_controller = None
	channels = [0,0,1,0] #Left, Right, Front, Rear
	filepath = ''

	
	def __init__(self, session, language, key):
		self.google_client = ASRClient(language, key)
		self.audio_recorder = session.service("ALAudioRecorder")
		self.leds_controller = ALProxy("ALLeds")
		
	def continuousRecognition(self,timeout):
		results = []
		while not results:
			self.startRecognition()
			self.leds_controller.randomEyes(timeout)
			time.sleep(timeout)
			results = self.stopRecognition()
		return results

	def startRecognition(self):
		self.audio_recorder.stopMicrophonesRecording()
		if self.recognizing:
			print '[ASR] Warning! Already recognizing..'
			return 0
		else:
			self.recognizing = True
			self.filepath = '/home/nao/test.wav'
			print self.filepath
			print os.path.abspath(self.filepath)
			self.audio_recorder.startMicrophonesRecording(self.filepath, "wav", 16000, self.channels)
			print '[ASR] Recording..'
			return 1
	
	def stopRecognition(self):
		if self.recognizing:
			self.recognizing = False
			self.audio_recorder.stopMicrophonesRecording()
			print '[ASR] Recognizing..'
			return self.google_client.recognize(os.path.abspath(self.filepath))
			
		else:
			print '[ASR] Warning! Already stopped..'
			return 0
