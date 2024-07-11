import qi
import argparse
import sys
import time
import os

# Simulated user data storage
user_data = {
    "Camilla": {"scared": True},
    "Claudio": {"scared": False},
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
    
    print("Starting ...")

    # Check if the user is recognized and scared
    if name in user_data and user_data[name]["scared"]:
        tts_service.say("Nice to see you again, {}! I remember last time you were very scared. Today, I'll tell you a less scary story.".format(name))
    else:
        tts_service.say("Nice to meet you, {}! Today, I'll tell you a story.".format(name))


    # Initial Story
    tts_service.say("Once upon a time, in a friendly forest, there was a little bunny named Bubbles. Bubbles loved to hop around and make new friends. One day, Bubbles found a shiny, magical flower.")

    # First Interactive Question
    tts_service.say("What should Bubbles do with the flower? Should Bubbles pick it up or leave it? ")
    choice1 = raw_input("Enter 1 to pick it up or 2 to leave it: ")

    if choice1 == '1':
        tts_service.say("Bubbles picked up the flower and suddenly, a rainbow appeared in the sky! Bubbles was excited and decided to follow the rainbow.")
        story_continuation = "Bubbles and Squeaky decided to explore the forest together. They heard a soft music coming from the bushes."
    elif choice1 == '2':
        tts_service.say("Bubbles left the flower and continued hopping around. Soon, Bubbles found a friendly squirrel named Squeaky who wanted to play.")
        story_continuation = "Bubbles and Squeaky decided to explore the forest together. They heard a soft music coming from the bushes."
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume Bubbles picks up the flower.")
        story_continuation = "Bubbles picked up the flower and suddenly, a rainbow appeared in the sky! Bubbles was excited and decided to follow the rainbow."

    tts_service.say(story_continuation)

    # Second Interactive Question
    tts_service.say("Should Bubbles and Squeaky follow the music or continue exploring? ")
    choice2 = raw_input("Enter 1 to follow the music or 2 to continue exploring: ")

    if choice2 == '1':
        tts_service.say("They followed the music and found a group of fairies having a picnic. The fairies invited them to join and they all had a wonderful time.")
    elif choice2 == '2':
        tts_service.say("They continued exploring and found a hidden pond with colorful fish. They played by the pond and enjoyed the beautiful day.")
    else:
        tts_service.say("Sorry, I didn't understand your choice. Let's assume they continue exploring.")
        tts_service.say("They continued exploring and found a hidden pond with colorful fish. They played by the pond and enjoyed the beautiful day.")

    tts_service.say("The end. I hope you enjoyed the story, {}!".format(name))

    print("End of the story")

if __name__ == "__main__":
    main()
