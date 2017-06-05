import os
from aiml.Kernel import Kernel
import argparse
import signal
from event_abstract import *


class DialogueManager(EventAbstractClass):
    PATH = ''
    EVENT_NAME = "VordReranked"

    def __init__(self, ip, port, aiml_path):
        super(self.__class__, self).__init__(self, ip, port)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.kernel = Kernel()
        self._learn(aiml_path)

    def start(self, *args, **kwargs):
        self.subscribe(
            event=DialogueManager.EVENT_NAME,
            callback=self.callback
        )

        print "Subscribers:", self.memory.getSubscribers(DialogueManager.EVENT_NAME)

        self._spin()

        self.unsubscribe(DialogueManager.EVENT_NAME)
        self.broker.shutdown()

    def callback(self, *args, **kwargs):
        print 'User says: ' + args[1]
        reply = self.kernel.respond(args[1][0])
        print 'Robot says: ' + reply
        self.memory.raiseEvent("VordReplied", reply)

    def _spin(self, *args):
        while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print 'Caught Ctrl+C, stopping.'
        self.__shutdown_requested = True
        print 'Good-bye'

    def _learn(self, path):
        print "Importing AIML KBs..."
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('aiml'):
                    self.kernel.learn(os.path.join(root, filename))
        print "...AIML KBs imported!"
        print 'Number of categories: ' + str(self.kernel.numCategories())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("-a", "--aiml-path", type=str, default="kbs",
                        help="Use one of the supported languages (only English at the moment)")
    args = parser.parse_args()

    dm = DialogueManager(
        ip=args.pip,
        port=args.pport,
        aiml_path=args.aiml_path
    )
    dm.update_globals(globals())
    dm.start()


if __name__ == "__main__":
    main()
