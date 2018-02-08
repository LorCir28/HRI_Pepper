import qi
import argparse
import sys
import time
import os



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--sentence", type=str, default="hello",
                        help="Sentence to say")
    parser.add_argument("--language", type=str, default="English",
                        help="language")
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    strsay = args.sentence
    language = args.language

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Memory Read", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    tts_service = session.service("ALTextToSpeech")

    tts_service.setLanguage(language)
    tts_service.say(strsay)
    print "  -- Say: "+strsay



if __name__ == "__main__":
    main()
