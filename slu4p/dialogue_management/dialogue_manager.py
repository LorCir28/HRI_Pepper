import os
from Kernel import Kernel
import argparse
import signal
import slu_utils
from event_abstract import *


class DialogueManager(EventAbstractClass):
    PATH = ''
    EVENT_NAME = "VRanked"

    def __init__(self, ip, port, aiml_path):
        super(self.__class__, self).__init__(self, ip, port)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.kernel = Kernel()
        self.__learn(aiml_path)

    def start(self, *args, **kwargs):
        self.subscribe(
            event=DialogueManager.EVENT_NAME,
            callback=self.callback
        )

        print "[" + self.inst.__class__.__name__ + "] Subscribers:", self.memory.getSubscribers(DialogueManager.EVENT_NAME)

        self._spin()

        self.unsubscribe(DialogueManager.EVENT_NAME)
        self.broker.shutdown()

    def callback(self, *args, **kwargs):
        transcriptions_dict = slu_utils.list_to_dict_w_probabilities(args[1])
        best_transcription = slu_utils.pick_best(transcriptions_dict)
        print "[" + self.inst.__class__.__name__ + "] User says: " + best_transcription
        reply = self.kernel.respond(best_transcription)
        print "[" + self.inst.__class__.__name__ + "] Robot says: " + reply
        self.memory.raiseEvent("Veply", reply)

    def _spin(self, *args):
        while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print "[" + self.inst.__class__.__name__ + "] Caught Ctrl+C, stopping."
        self.__shutdown_requested = True
        print "[" + self.inst.__class__.__name__ + "] Good-bye"

    def __learn(self, path):
        for root, directories, file_names in os.walk(path):
            for filename in file_names:
                if filename.endswith('.aiml'):
                    self.kernel.learn(os.path.join(root, filename))
        print "[" + self.inst.__class__.__name__ + "] Number of categories: " + str(self.kernel.num_categories())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("-a", "--aiml-path", type=str, default="resources/aiml_kbs",
                        help="Path to the root folder of AIML Knowledge Base")
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
