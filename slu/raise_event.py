import qi
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.pip + ":" + str(args.pport))
    except RuntimeError:
        print 'ERROR'
        # print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) + ".\n"
        # "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    memory = session.service("ALMemory")
    d = {'GoogleASR': ['move to the feet', 'more to the fridge', 'move to the fridge', 'move to the fate',
                       'move to the finch'], 'NuanceASR': ['move to the fridge']}
    memory.raiseEvent("VordRecognized", d)


if __name__ == "__main__":
    main()
