import qi
import argparse
import sys
import time
import os

'''
def getenv(envstr, def = None):
    if envstr in os.environ:
        return os.environ[envstr]
    else:
        return def
'''

#getenv('PEPPER_IP','127.0.0.1'),
#default=getenv('PEPPER_PORT',9559),

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default= '127.0.0.1',
                        help="Robot IP address.  On robot or Local Naoqi: use 127.0.0.1.")
    parser.add_argument("--pport", type=int, default=50381,
                        help="Naoqi port number (default: 9559)")
    parser.add_argument("--sentence", type=str, default="hello",
                        help="Sentence to say")
    parser.add_argument("--language", type=str, default="English",
                        help="language")
    parser.add_argument("--speed", type=int, default=1000,
                        help="speed")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    strsay = args.sentence
    language = args.language
    speed = args.speed

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

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)
    tts_service.say(strsay)
    #print "  -- Say: "+strsay
    tts_service.say("What is your name?")
    name = raw_input("Please enter your name: ")
    tts_service.say("Nice to meet you, {}! I have an interesting story to tell you.".format(name))

    print("Starting ...")

    # Initial Story
    tts_service.say("Once upon a time, in a village near the mountains, there was a brave girl named Emma. Emma loved adventures. One day, she found a mysterious cave near her village.")

    # First Interactive Question
    tts_service.say("What should Emma do? Should she enter the cave or go back to the village? Please type 1 to enter the cave or 2 to go back to the village.")
    choice1 = raw_input("Enter 1 to enter the cave or 2 to go back to the village: ")

    if choice1 == '1':
        tts_service.say("Emma entered the cave and saw glittering crystals on the walls. She noticed a faint light deeper inside.")
        story_continuation = "Inside the cave, Emma found an old map with a riddle."
    elif choice1 == '2':
        tts_service.say("Emma went back to the village and told her friends about the cave. Her friends decided to join her and explore the cave together.")
        story_continuation = "Inside the cave, Emma and her friends found an old map with a riddle."
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume Emma enters the cave.")
        story_continuation = "Inside the cave, Emma found an old map with a riddle."

    tts_service.say(story_continuation)

    # Second Interactive Question
    tts_service.say("Should they try to solve the riddle or continue exploring the cave? Please type 1 to solve the riddle or 2 to continue exploring.")
    choice2 = raw_input("Enter 1 to solve the riddle or 2 to continue exploring: ")

    if choice2 == '1':
        tts_service.say("They solved the riddle and found a hidden treasure chest full of gold coins. They were thrilled with their discovery.")
    elif choice2 == '2':
        tts_service.say("They continued exploring and found a beautiful underground lake with glowing water. They played by the lake and had an unforgettable adventure.")
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume they continue exploring.")
        tts_service.say("They continued exploring and found a beautiful underground lake with glowing water. They played by the lake and had an unforgettable adventure.")

    tts_service.say("The end. I hope you enjoyed the story, {}!".format(name))

    print("End of the story")

if __name__ == "__main__":
    main()
