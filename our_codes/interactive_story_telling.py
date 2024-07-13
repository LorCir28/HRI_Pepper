import qi
import argparse
import sys
import time
import os


def wave_hello(motion_service):
    # Enable the arms control by the pose manager.
    motion_service.setStiffnesses("LArm", 1.0)
    
    # Move the left arm to wave hello
    names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
    angles = [-0.7, 0.3, -1.0, -0.5, 0.3]  # Adjusted angles to raise the arm higher
    times = [1.0, 1.0, 1.0, 1.0, 1.0]  # Time in seconds to reach the position
    
    # Move the arm up
    motion_service.angleInterpolation(names, angles, times, True)
    
    # Wave the hand
    for _ in range(3):
        motion_service.setAngles("LElbowYaw", -1.0, 0.2)
        time.sleep(0.5)
        motion_service.setAngles("LElbowYaw", -0.8, 0.2)
        time.sleep(0.5)
    
    # Return the arm to a neutral position
    angles = [1.5, 0.3, -1.3, -1.0, 0.0]  # Neutral position angles
    motion_service.angleInterpolation(names, angles, times, True)
    
    # Disable the arms control by the pose manager.
    motion_service.setStiffnesses("LArm", 0.0)


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
    memory_service = session.service("ALMemory")
    motion_service = session.service("ALMotion")

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)
    tts_service.setParameter("speed", speed)
    # tts_service.say(strsay)
    tts_service.say("Hello, What is your name?")
    user = raw_input("Please enter your name: ")

    recognized_user = False

    try:
        # KNOWN USER 
        known_user = memory_service.getData(user)
        tts_service.say("Hello" + " "  + known_user + ", I can recognize you!!")
        wave_hello(motion_service)
        recognized_user = True

    except:
        # UNKNOWN USER
        memory_service.insertData(user, user)
        tts_service.say('Hello' + ' ' + user + ', nice to meet you for the first time!!')
        wave_hello(motion_service)
        tts_service.say('I will tell you a story')

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

        tts_service.say("The end. I hope you enjoyed the story!")
        tts_service.say('a last question: Have you been scared by this story?')
        choice3 = raw_input("Enter 1 for yes or 2 for no: ")

        if choice3 == '1':
            memory_service.insertData(user, 'scared')
        else:
            memory_service.insertData(user, 'not scared')

        tts_service.say('Bye bye, see you next time!!')
        wave_hello(motion_service)


    # KNOWN USER
    if recognized_user:
        # tts_service.say('Hello' + ' ' + user + ', I can recognize you!!')
        val = memory_service.getData(user)

        # USER SPAVENTATO
        if val == 'scared':
            tts_service.say('since the last time you were scared about my story, now I will tell you a less scary one')

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

            tts_service.say("The end. I hope you enjoyed the story!")

            tts_service.say('Bye bye, see you next time!!')
            wave_hello(motion_service)




        # USER NON SPAVENTATO
        elif val == 'not scared':
            tts_service.say('since the last time you were not scared about my story, now I will tell you a more scary one')
    
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

            tts_service.say("The end. I hope you enjoyed the story!")
    
            tts_service.say('Bye bye, see you next time!!')
            wave_hello(motion_service)





if __name__ == "__main__":
    main()
