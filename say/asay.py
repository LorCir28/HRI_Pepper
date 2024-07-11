import qi
import argparse
import sys
import time
import os


def getenv(envstr, def=None):
    if envstr in os.environ:
        return os.environ[envstr]
    else:
        return def

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=getenv('PEPPER_IP','127.0.0.1'),
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=getenv('PEPPER_PORT',9559),
                        help="Naoqi port number (default: 9559)")
    parser.add_argument("--sentence", type=str, default="hello",
                        help="Sentence to say")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    strsay = args.sentence

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Say", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    ans_service = session.service("ALAnimatedSpeech")
    configuration = {"bodyLanguageMode":"contextual"}

    ans_service.say(strsay, configuration)
    print "  -- Animated Say: "+strsay



if __name__ == "__main__":
    main()
