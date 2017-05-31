import os
import requests
import urllib
import requests
import json
import sys
import tempfile
import time
from speech.google_client import GoogleClient

class SpeechRecognition:

	recognizing = False
	google_client = None
	nuance_client = None
	mem_service = None
	audio_recorder = None
	leds_controller = None
	vocabulary = []
	channels = [0,0,1,0] #Left, Right, Front, Rear
	filepath = ''

	
	def __init__(self, session, language, key, vocabulary_file):
		self.google_client = GoogleClient(language, key)
		self.audio_recorder = session.service("ALAudioRecorder")
		self.nuance_client = session.service("ALSpeechRecognition")
		self.nuance_client.pause(True)
		with open(vocabulary_file) as f:
			self.vocabulary = f.readlines()
		self.vocabulary = [x.strip() for x in self.vocabulary]
		self.nuance_client.setLanguage("English")
		self.nuance_client.setVocabulary(self.vocabulary, False)
		self.mem_service = session.service("ALMemory")
		self.subscriber = self.mem_service.subscriber("SpeechDetected")
		self.subscriber.signal.connect(self.callback)
		#self.leds_controller = ALProxy("ALLeds")
	
	def callback(self, value):
		print value
		if value == 1:
			time.sleep(2)
			print self.stopRecognition()
	
	def continuousRecognition(self,timeout):
		results = []
		while not results:
			self.startRecognition()
			time.sleep(1)
			#results = self.stopRecognition()
			return results

	def startRecognition(self):
		self.nuance_client.pause(False)
		self.nuance_client.subscribe('NuanceSpeechRecognition')
		self.audio_recorder.stopMicrophonesRecording()
		if self.recognizing:
			print '[SpeechRecognition] Warning! Already recognizing..'
			return 0
		else:
			self.recognizing = True
			#self.nuance_client.subscribe("Test_SpeechRecognition")
			self.filepath = '/home/nao/test.wav'
			self.audio_recorder.startMicrophonesRecording(self.filepath, "wav", 16000, self.channels)
			print '[SpeechRecognition] Recording..'
			return 1
	
	def stopRecognition(self):
		self.nuance_client.pause(True)
		self.nuance_client.unsubscribe('NuanceSpeechRecognition')
		if self.recognizing:
			self.recognizing = False
			self.audio_recorder.stopMicrophonesRecording()
			print '[SpeechRecognition] Recognizing..'
			google_results = []
			#google_results = self.google_client.recognize(os.path.abspath(self.filepath))
			nuance_results = self.mem_service.getData("WordRecognized")[0]
			google_results.append(nuance_results)
			return google_results
			
		else:
			print '[SpeechRecognition] Warning! Already stopped..'
			return 0
