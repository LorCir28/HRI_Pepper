import qi
import argparse
import sys
import os
import signal
from functools import partial

def signal_handler(ap_service, signal, frame):
        print('Quitting')
        ap_service.stopAll()
        sys.exit(0)
        


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--afile", type=str, help="Audio file to play")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    afile = args.afile

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        print "Connecting to ",	connection_url
        app = qi.Application(["Memory Write", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session
    
    #Starting services
    ap_service = session.service("ALAudioPlayer")

    signal.signal(signal.SIGINT, partial(signal_handler, ap_service))
    
    #Loads a file and launchs the playing 5 seconds later
    fileId = ap_service.loadFile(os.path.abspath(afile))
    ap_service.play(fileId)
    print 'Playing'+afile+'. Press Ctrl+C to stop'




if __name__ == "__main__":
    main()
