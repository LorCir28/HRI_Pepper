import argparse
import signal
from naoqi import ALProxy, ALBroker, ALModule
from event_abstract import *


class TextToSpeech(EventAbstractClass):
    PATH = ''
    EVENT_NAME = "Veply"

    def __init__(self, ip, port, body_language_mode):
        super(self.__class__, self).__init__(self, ip, port)
        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)
        self.tts = ALProxy("ALAnimatedSpeech")
        self.configuration = {"bodyLanguageMode": body_language_mode}

    def start(self, *args, **kwargs):
        self.subscribe(
            event=TextToSpeech.EVENT_NAME,
            callback=self.callback
        )

        print "Subscribers:", self.memory.getSubscribers(TextToSpeech.EVENT_NAME)

        self._spin()

        self.unsubscribe(TextToSpeech.EVENT_NAME)
        self.broker.shutdown()

    def callback(self, *args, **kwargs):

        self.tts.say(args[1], self.configuration)

    def _spin(self, *args):
        while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print 'Caught Ctrl+C, stopping.'
        self.__shutdown_requested = True
        print 'Good-bye'


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("-l", "--language-mode", type=str, default="contextual",
                        help="The body language modality while speaking",
                        choices=['contextual', 'random', 'disabled'])

    args = parser.parse_args()

    tts = TextToSpeech(
        ip=args.pip,
        port=args.pport,
        body_language_mode=args.language_mode
    )
    tts.update_globals(globals())
    tts.start()


if __name__ == "__main__":
    main()
