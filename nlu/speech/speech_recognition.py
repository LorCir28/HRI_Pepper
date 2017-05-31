import time
import signal
import argparse
import yaml
import os

from naoqi import ALProxy, ALBroker, ALModule
from abc import ABCMeta
from speech.google_client import *
from event_abstract import *

class SpeechRecognition(EventAbstractClass):
    EVENT_NAME = "WordRecognized"
    google_client = None
    audio_recorder = None
    filepath = '/home/nao/test.wav'
    channels = [0,0,1,0]
    GOOGLE_KEY = 'AIzaSyAONQ_K4NOIGfRWXmiuXonThf2rs3XzKPY'
	#GOOGLE_KEY = 'AIzaSyDya-9naDiG0Dm8MVVKhQw50HmsvfZeZfE'

    def __init__(self, filename, ip, port, language, word_spotting, audio, visual):
        super(self.__class__, self).__init__(self.__class__.__name__, ip, port)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.asr = ALProxy("ALSpeechRecognition")
        print self.asr.getAvailableLanguages()
        
        self.audio_recorder = ALProxy("ALAudioRecorder")
        
        vocabulary = self.read_vocabulary(filename)
        #print "Using vocabulary: %s" % vocabulary
        if (language == 'en') or (language == 'eng') or (language == 'english') or (language == 'English'):
        	nuance_language = 'English'
        	google_language = "en-US"
        	
        self.configure(
            vocabulary=vocabulary,
            nuance_language=nuance_language,
            google_language=google_language,
            word_spotting=word_spotting,
            audio=audio,
            visual=visual
        )
    
    def start(self):
    	self.subscribe(
            event=SpeechRecognition.EVENT_NAME,
            callback=self.callback
        )

        print "Subscribers:", self.memory.getSubscribers(SpeechRecognition.EVENT_NAME)
        
        self.audio_recorder.stopMicrophonesRecording()
        self.audio_recorder.startMicrophonesRecording(self.filepath, "wav", 16000, self.channels)

        self._spin()

        self.unsubscribe(SpeechRecognition.EVENT_NAME)
        self.broker.shutdown()
    
    def stop(self):
        self.audio_recorder.stopMicrophonesRecording()
        self.__shutdown_requested = True
        print 'Good-bye'

    def configure(self, vocabulary, word_spotting, nuance_language, google_language, audio, visual):
        self.asr.pause(True)
        self.asr.setVocabulary(vocabulary, word_spotting)
        self.asr.setLanguage(nuance_language)
        self.asr.setAudioExpression(audio)
        self.asr.setVisualExpression(visual)
        self.asr.pause(False)
        self.google_client = GoogleClient(google_language, self.GOOGLE_KEY)
    
    def callback(self, *args, **kwargs):
    	self.audio_recorder.stopMicrophonesRecording()
    	results = []
    	results = self.google_client.recognize(os.path.abspath(self.filepath))
    	if args[1][1] > 0.5:
    		results.append(args[1][0])
    	print results
    	if 'bye' in results:
    		self.stop()
        self.audio_recorder.startMicrophonesRecording(self.filepath, "wav", 16000, self.channels)

    def read_vocabulary(self, vocabulary_file):
        with open(vocabulary_file) as f:
            vocabulary = f.readlines()
        return [x.strip() for x in vocabulary]

    def _spin(self, *args):
    	while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print 'Caught Ctrl+C, stopping.'
        self.audio_recorder.stopMicrophonesRecording()
        self.__shutdown_requested = True
        print 'Good-bye'

def main():
	
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("-l", "--lang", type=str, default="en",
                        help="Use one of the supported languages (only English at the moment)")
    parser.add_argument("-w", "--word-spotting", action="store_true",
                        help="Run in word spotting mode")
    parser.add_argument("-a", "--no-audio", action="store_true",
                        help="Turn off bip sound when recognition starts")
    parser.add_argument("-v", "--no-visual", action="store_true",
                        help="Turn off blinking eyes when recognition starts")
    parser.add_argument("vocabulary_file", type=str, help="A txt file containing the list of sentences composing the vocabulary.")
    args = parser.parse_args()

    sr = SpeechRecognition(
        filename=args.vocabulary_file,
        ip=args.pip,
        port=args.pport,
        language=args.lang,
        word_spotting=args.word_spotting,
        audio=not args.no_audio,
        visual=not args.no_visual
        )
    sr.start()
	
if __name__ == "__main__":
	main()
