import qi
import argparse
import sys
import time
import os


# user = 'Camilla'
user = 'Claudio'
# user = 'Lorenzo'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1',
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=55776,
                        help="Naoqi port number (default: 9559)")
    parser.add_argument("--sentence", type=str, default="hello Claudio",
                        help="Sentence to say")
    parser.add_argument("--language", type=str, default="English",
                        help="language")
    parser.add_argument("--speed", type=int, default=2000,
                        help="speed")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    language = args.language
    speed = 10

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

    tts_service = session.service("ALTextToSpeech")
    memory_service  = session.service("ALMemory")

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)

    # known_users = [] # array to save users

    try:
        val = memory_service.getData(user)
        strsay = 'Hello' + ' ' + user + ', I can recognize you!!'
    except:
        memory_service.insertData(user,user)
        strsay = 'Hello' + ' ' + user + ', nice to meet you for the first time!!'
        
    # if memory_service.getData(user):
    #     strsay = 'Hello' + ' ' + user + ', I can recognize you!!'
    # else:
    #     known_users.append(user)
    #     strsay = 'Hello' + ' ' + user + ', nice to meet you for the first time!!'

    tts_service.say(strsay)
    tts_service.say(strsay)
    tts_service.say(strsay)

    print"  -- Say: "+strsay




if __name__ == "__main__":
    main()


