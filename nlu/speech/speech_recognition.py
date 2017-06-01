import argparse
import os
import signal
from naoqi import ALProxy, ALBroker, ALModule
from speech.google_client import *
from event_abstract import *


class SpeechRecognition(EventAbstractClass):
    EVENT_NAME = "WordRecognized"
    FLAC_CONV = 'flac -f '
    FILE_PATH = '/tmp/recording'
    CHANNELS = [0, 0, 1, 0]

    def __init__(self, ip, port, language, word_spotting, audio, visual, vocabulary_file, google_keys):
        super(self.__class__, self).__init__(self, ip, port)
        # self._make_global(self.__class__.__name__+"_inst", self)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.nuance_asr = ALProxy("ALSpeechRecognition")

        self.audio_recorder = ALProxy("ALAudioRecorder")

        vocabulary = self.read_vocabulary(vocabulary_file)
        if (language == 'en') or (language == 'eng') or (language == 'english') or (language == 'English'):
            nuance_language = 'English'
            google_language = "en-US"

        self.configure(
            vocabulary=vocabulary,
            nuance_language=nuance_language,
            google_language=google_language,
            word_spotting=word_spotting,
            audio=audio,
            visual=visual,
            keys=google_keys
        )

    def start(self, *args, **kwargs):
        self.subscribe(
            event=SpeechRecognition.EVENT_NAME,
            callback=self.callback
        )

        print "Subscribers:", self.memory.getSubscribers(SpeechRecognition.EVENT_NAME)

        self.audio_recorder.stopMicrophonesRecording()
        self.audio_recorder.startMicrophonesRecording(self.FILE_PATH + ".wav", "wav", 16000, self.CHANNELS)

        self._spin()

        self.unsubscribe(SpeechRecognition.EVENT_NAME)
        self.broker.shutdown()

    def stop(self):
        self.audio_recorder.stopMicrophonesRecording()
        self.__shutdown_requested = True
        print 'Good-bye'

    def configure(self, word_spotting, nuance_language, google_language, audio, visual, vocabulary, keys):
        self.nuance_asr.pause(True)
        self.nuance_asr.setVocabulary(vocabulary, word_spotting)
        self.nuance_asr.setLanguage(nuance_language)
        self.nuance_asr.setAudioExpression(audio)
        self.nuance_asr.setVisualExpression(visual)
        self.nuance_asr.pause(False)
        self.google_asr = GoogleClient(google_language, keys)

    def callback(self, *args, **kwargs):
        self.audio_recorder.stopMicrophonesRecording()
        """
        Convert Wave file into Flac file
        """
        os.system(self.FLAC_CONV + self.FILE_PATH + '.wav')
        f = open(self.FILE_PATH + '.flac', 'rb')
        flac_cont = f.read()
        f.close()

        results = [r.encode('ascii', 'ignore') for r in self.google_asr.recognize_data(flac_cont)]
        if args[1][1] > 0.5:
            results.append(args[1][0])
        print results
        if 'bye' in results:
            self.stop()
        self.audio_recorder.startMicrophonesRecording(self.FILE_PATH + ".wav", "wav", 16000, self.CHANNELS)
        self.memory.raiseEvent("VordRecognized", results)

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
    parser.add_argument("--word-spotting", action="store_true",
                        help="Run in word spotting mode")
    parser.add_argument("--no-audio", action="store_true",
                        help="Turn off bip sound when recognition starts")
    parser.add_argument("--no-visual", action="store_true",
                        help="Turn off blinking eyes when recognition starts")
    parser.add_argument("-v", "--vocabulary", type=str, default="vocabulary.txt",
                        help="A txt file containing the list of sentences composing the vocabulary.")
    parser.add_argument("-k", "--keys", type=str, default="google_keys.txt",
                        help="A txt file containing the list of the keys for the Google ASR.")
    args = parser.parse_args()

    sr = SpeechRecognition(
        ip=args.pip,
        port=args.pport,
        language=args.lang,
        word_spotting=args.word_spotting,
        audio=not args.no_audio,
        visual=not args.no_visual,
        vocabulary_file=args.vocabulary,
        google_keys=args.keys
    )
    sr.update_globals(globals())
    sr.start()


if __name__ == "__main__":
    main()
