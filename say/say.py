import qi
import argparse
import sys
import time
import os



def phraseToSay(params):
    if (params=='hello'):
        return "Hello!"
    elif (params=='greetperson'):
        tosay = "Hello person!"
        return tosay
    elif (params=='starting'):
        return "OK. Let's start!"
    elif (params=='personnotfound'):
        return "It seems there is nobody around here!"
    elif (params=='goodbye'):
        return "Goodbye! See you soon!"
    elif (params=='carhere'):
        return "OK! I am marking this location as the car position"
    elif (params=='whatnow'):
        return "What do you want me to do now?"
    elif (params=='lookatme'):
        return "Please, can you look at me for some seconds"
    elif (params=='readytofollow'):
        return "OK,I am ready to follow you. Let's go"
    elif (params=='lookforhelp'):
        return "I'm looking for some help, I'm coming in a while"
    elif (params=='arrivedcar'):
        return "We just arrived to the car, thank you for coming to help"
    elif (params=='followme'):
        return "Please, follow me to the car"
    elif (params=='comehere'):
        return "I cannot see you, could you come here please?"
    return "Nothing to say."



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

    tosay = phraseToSay(strsay)
    tts_service.say(strsay)
    print "  -- Say: "+strsay



if __name__ == "__main__":
    main()
