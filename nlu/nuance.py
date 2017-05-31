import time
import signal
import argparse
from naoqi import ALProxy, ALBroker, ALModule
import yaml
from abc import ABCMeta
from speech.google_client import *
import os

class EventAbstractClass(ALModule):
    __metaclass__ = ABCMeta

    def __init__(self, name, ip, port):
        self.name = name
        self._make_global(self.name, self)
        self.broker = self._connect(name, ip, port)
        super(EventAbstractClass, self).__init__(self.name)

        self.memory = self._make_global("memory", ALProxy("ALMemory"))

    def _connect(self, name, ip, port):
        try:
            broker = ALBroker(name + "_broker",
               "0.0.0.0",   # listen to anyone
               0,           # find a free port and use it
               ip,         # parent broker IP
               port)
            print "Connected to %s:%s" % (ip, str(port))
            return broker
        except RuntimeError:
            print "Cannot connect to %s:%s. Retrying in 1 second." % (ip, str(port))
            time.sleep(1)
            return self._connect(name, ip, port)

    def _make_global(self, name, var):
        globals()[name] = var
        return globals()[name]

    def subscribe(self, event, callback):
        self.memory.subscribeToEvent(
            event,
            self.name,
            callback.func_name
        )

    def unsubscribe(self, event):
        self.memory.unsubscribeToEvent(
            event,
            self.name
        )

    def remove_subscribers(self, event):
        subscribers = self.memory.getSubscribers(event)
        if subscribers:
            print "Speech recognition already in use by another node"
            for module in subscribers:
                self.__stop_module(module, event)

    def __stop_module(self, module, event):
        print "Unsubscribing '{}' from NAO speech recognition".format(
            module)
        try:
            self.memory.unsubscribeToEvent(event, module)
        except RuntimeError:
            print "Could not unsubscribe from NAO speech recognition"


class SpeechRecognitionTest(EventAbstractClass):
    EVENT_NAME = "WordRecognized"
    google_client = None
    audio_recorder = None
    filepath = '/home/nao/test.wav'
    channels = [0,0,1,0]

    def __init__(self, filename, ip, port, language, word_spotting, audio, visual):
        super(self.__class__, self).__init__(self.__class__.__name__, ip, port)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.asr = ALProxy("ALSpeechRecognition")
        print self.asr.getAvailableLanguages()
        
        self.audio_recorder = ALProxy("ALAudioRecorder")
        

        vocabulary = self.read_vocabulary(filename)
        print "Using vocabulary: %s" % vocabulary
        self.configure(
            vocabulary=vocabulary,
            language=language,
            word_spotting=word_spotting,
            audio=audio,
            visual=visual
        )
        self.google_client = GoogleClient('en-US', 'AIzaSyAONQ_K4NOIGfRWXmiuXonThf2rs3XzKPY')
    
    def start(self):
    	
    	self.subscribe(
            event=SpeechRecognitionTest.EVENT_NAME,
            callback=self.callback
        )

        print "Subscribers:", self.memory.getSubscribers(SpeechRecognitionTest.EVENT_NAME)
        
        self.audio_recorder.stopMicrophonesRecording()
        self.audio_recorder.startMicrophonesRecording(self.filepath, "wav", 16000, self.channels)

        self._spin()

        self.unsubscribe(SpeechRecognitionTest.EVENT_NAME)
        self.broker.shutdown()
    
    def stop(self):
        self.audio_recorder.stopMicrophonesRecording()
        self.__shutdown_requested = True
        print 'Good-bye'

    def configure(self, vocabulary, word_spotting, language, audio, visual):
        self.asr.pause(True)
        self.asr.setVocabulary(vocabulary, word_spotting)
        self.asr.setLanguage(language)
        self.asr.setAudioExpression(audio)
        self.asr.setVisualExpression(visual)
        self.asr.pause(False)


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

    def read_vocabulary(self, f):
        with open(f, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as e:
                print e

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


if __name__ == "__main__":

    languages = ["English"]

    parser = argparse.ArgumentParser()
    parser.add_argument("vocabulary_file", type=str, help="A yaml file containing the list of words for the vocabulary.")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--language", type=str, default="English",
                        help="Use one of the supported languages: %s" % languages)
    parser.add_argument("--word-spotting", action="store_true",
                        help="Run in word spotting mode")
    parser.add_argument("--no-audio", action="store_true",
                        help="Turn off bip sound when recognition starts")
    parser.add_argument("--no-visual", action="store_true",
                        help="Turn off blinking eyes when recognition starts")
    args = parser.parse_args()

    if args.language in languages:
        s = SpeechRecognitionTest(
            filename=args.vocabulary_file,
            ip=args.ip,
            port=args.port,
            language=args.language,
            word_spotting=args.word_spotting,
            audio=not args.no_audio,
            visual=not args.no_visual
            )
        s.start()
    else:
        print "Unsupported language: '%s'. Please use -h to learn more." % args.language