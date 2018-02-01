#http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

import qi
import argparse
import sys
import time
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--image", type=str, default="default.jpg",
                        help="Image to show (in spqrel_apps/html/img folder)")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    imfile = args.image

    #Start working session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    tablet_service = session.service("ALTabletService")

    # Display a local image located in img folder in the root of the web server
    # The ip of the robot from the tablet is 198.18.0.1
    tablet_service.showImage("http://198.18.0.1/apps/spqrel/img/%s" %(imfile))

    #tablet_service.showWebview("http://198.18.0.1/apps/spqrel")

    #time.sleep(10)

    # Hide the web view
    # tablet_service.hideImage()

if __name__ == "__main__":
    main()

