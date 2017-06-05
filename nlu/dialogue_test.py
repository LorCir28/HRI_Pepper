import argparse
from aiml.dialogue_manager import DialogueManager


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
