#http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

import qi
import argparse
import sys
import os
import math

commands = [ ['F', 620, 130], ['B', 620, 500], ['L', 480, 310], ['R', 820, 310],
['OK', 620, 310], ['X', 480, 500], ['A', 620, 500] ]


# function called when the signal onTouchDown is triggered
def onTouched(x, y):
    print "coordinates are x: ", x, " y: ", y
    mind=200
    cmd = ''
    for a in commands:
        d = abs(x - a[1]) + abs(y - a[2])
        if (d < mind):
            mind = d
            cmd = a[0]
    print 'Sapientino key: ',cmd

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["TabletModule", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    tablet_service = session.service("ALTabletService")

    idTTouch = tablet_service.onTouchDown.connect(onTouched)
    app.run()    



if __name__ == "__main__":
    main()
