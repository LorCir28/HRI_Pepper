from speech.speech_recognition import *


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
