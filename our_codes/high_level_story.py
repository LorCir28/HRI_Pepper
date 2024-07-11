import qi
import argparse
import sys
import time
import os

# Simulated user data storage
user_data = {
    "Camilla": {"scared": False},
    "Claudio": {"scared": True},
    "Lorenzo": {"scared": False}
}

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

    # Check if the user is recognized and scared
    if name in user_data and not user_data[name]["scared"]:
        tts_service.say("Nice to see you again, {}! I remember last time you were very brave. Today, I'll tell you a scarier story.".format(name))
    else:
        tts_service.say("Nice to meet you, {}! Today, I'll tell you a story.".format(name))


    print("Starting ...")

    # Initial Story
    tts_service.say("Once upon a time, there was a small town with an old, abandoned house on the hill. People said it was haunted. One night, a brave boy named Jack decided to investigate the house.")

    # First Interactive Question
    tts_service.say("What should Jack do first? Should he enter the house through the front door or check the windows?")
    choice1 = raw_input("Enter 1 to enter through the front door or 2 to check the windows: ")

    if choice1 == '1':
        tts_service.say("Jack entered through the front door and heard a creaking noise. He saw shadows moving in the hallway.")
        story_continuation = "Inside the house, Jack found an old diary with entries about strange occurrences."
    elif choice1 == '2':
        tts_service.say("Jack checked the windows and saw flickering lights inside. He decided to enter through a broken window.")
        story_continuation = "Inside the house, Jack found an old diary with entries about strange occurrences."
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume Jack enters through the front door.")
        story_continuation = "Jack entered through the front door and heard a creaking noise. He saw shadows moving in the hallway."

    tts_service.say(story_continuation)

    # Second Interactive Question
    tts_service.say("Should Jack read the diary or explore the house further?")
    choice2 = raw_input("Enter 1 to read the diary or 2 to explore the house: ")

    if choice2 == '1':
        tts_service.say("Jack read the diary and learned about the house's history. Suddenly, he felt a cold breeze and saw a ghostly figure approaching.")
    elif choice2 == '2':
        tts_service.say("Jack continued exploring and found a hidden staircase leading to the basement. He heard whispers and felt a presence behind him.")
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume Jack reads the diary.")
        tts_service.say("Jack read the diary and learned about the house's history. Suddenly, he felt a cold breeze and saw a ghostly figure approaching.")

    tts_service.say("The end. I hope you enjoyed the story, {}!".format(name))

    print("End of the story")

if __name__ == "__main__":
    main()
