import qi
import argparse
import json
import sys
import time
import os
from speech.speech_recognition import *

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