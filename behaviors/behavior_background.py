import sys
import time
import argparse
import os
import qi

from naoqi import ALProxy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    
    args = parser.parse_args()

    #Starting application
    try:
        connection_url = "tcp://" + args.pip + ":" + str(args.pport)
        app = qi.Application(["Behavior ", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.pip + "\" on port " + str(args.pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()

    bm_service = app.session.service("ALBackgroundMovement")
    bm_service.setEnabled(True)

    ba_service = app.session.service("ALBasicAwareness")
    ba_service.setEnabled(True)

if __name__ == "__main__":
    main()

