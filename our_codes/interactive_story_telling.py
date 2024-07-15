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

def speak(tts_service, message, speed):
    tts_service.setParameter("speed", speed)
    tts_service.say(message)
    # Fixed short delay between speech segments
    time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default='127.0.0.1',
                        help="Robot IP address. On robot or Local Naoqi: use 127.0.0.1.")
    parser.add_argument("--pport", type=int, default=52400,
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

    # Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Say", "--qi-url=" + connection_url])
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) + ".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    tts_service = session.service("ALTextToSpeech")
    memory_service = session.service("ALMemory")
    motion_service = session.service("ALMotion")

    tts_service.setLanguage(language)
    tts_service.setVolume(1.0)

    speak(tts_service, "Hello, What is your name?", speed)
    user = raw_input("Please enter your name: ")

    recognized_user = False

    try:
        # KNOWN USER 
        known_user = memory_service.getData(user)
        speak(tts_service, "Hello " + known_user + ", I can recognize you!!", speed)
        wave_hello(motion_service)
        recognized_user = True

    except Exception:
        # UNKNOWN USER
        memory_service.insertData(user, user)
        speak(tts_service, 'Hello ' + user + ', nice to meet you for the first time!!', speed)
        wave_hello(motion_service)
        speak(tts_service, 'I will tell you a story', speed)

        speak(tts_service, "Once upon a time, in a village near the mountains, there was a brave girl named Emma. Emma loved adventures. One day, she found a mysterious cave near her village.", speed)

        # First Interactive Question
        speak(tts_service, "What should Emma do? Should she enter the cave or go back to the village? Please type 1 to enter the cave or 2 to go back to the village.", speed)
        choice1 = raw_input("Enter 1 to enter the cave or 2 to go back to the village: ")

        if choice1 == '1':
            speak(tts_service, "Emma entered the cave and saw glittering crystals on the walls. She noticed a faint light deeper inside.", speed)
            story_continuation = "Inside the cave, Emma found an old map with a riddle."
        elif choice1 == '2':
            speak(tts_service, "Emma went back to the village and told her friends about the cave. Her friends decided to join her and explore the cave together.", speed)
            story_continuation = "Inside the cave, Emma and her friends found an old map with a riddle."
        else:
            speak(tts_service, "Sorry, I didn't understand your choice. Let's assume Emma enters the cave.", speed)
            story_continuation = "Inside the cave, Emma found an old map with a riddle."

        speak(tts_service, story_continuation, speed)

        # Second Interactive Question
        speak(tts_service, "Should they try to solve the riddle or continue exploring the cave? Please type 1 to solve the riddle or 2 to continue exploring.", speed)
        choice2 = raw_input("Enter 1 to solve the riddle or 2 to continue exploring: ")

        if choice2 == '1':
            speak(tts_service, "They solved the riddle and found a hidden treasure chest full of gold coins. They were thrilled with their discovery.", speed)
        elif choice2 == '2':
            speak(tts_service, "They continued exploring and found a beautiful underground lake with glowing water. They played by the lake and had an unforgettable adventure.", speed)
        else:
            speak(tts_service, "Sorry, I didn't understand your choice. Let's assume they continue exploring.", speed)
            speak(tts_service, "They continued exploring and found a beautiful underground lake with glowing water. They played by the lake and had an unforgettable adventure.", speed)

        speak(tts_service, "The end. I hope you enjoyed the story!", speed)
        speak(tts_service, 'a last question: Have you been scared by this story?', speed)
        choice3 = raw_input("Enter 1 for yes or 2 for no: ")

        if choice3 == '1':
            memory_service.insertData(user, 'scared')
        else:
            memory_service.insertData(user, 'not scared')

        speak(tts_service, 'Bye bye, see you next time!!', speed)
        wave_hello(motion_service)

    # KNOWN USER
    if recognized_user:
        val = memory_service.getData(user)

        if val == 'scared':
            speak(tts_service, 'since the last time you were scared about my story, now I will tell you a less scary one', speed)

            # Initial Story
            speak(tts_service, "Once upon a time, there was a small town with an old, abandoned house on the hill. People said it was haunted. One night, a brave boy named Jack decided to investigate the house.", speed)

            # First Interactive Question
            speak(tts_service, "What should Jack do first? Should he enter the house through the front door or check the windows?", speed)
            choice1 = raw_input("Enter 1 to enter through the front door or 2 to check the windows: ")

            if choice1 == '1':
                speak(tts_service, "Jack entered through the front door and heard a creaking noise. He saw shadows moving in the hallway.", speed)
                story_continuation = "Inside the house, Jack found an old diary with entries about strange occurrences."
            elif choice1 == '2':
                speak(tts_service, "Jack checked the windows and saw flickering lights inside. He decided to enter through a broken window.", speed)
                story_continuation = "Inside the house, Jack found an old diary with entries about strange occurrences."
            else:
                speak(tts_service, "Sorry, I didn't understand your choice. Let's assume Jack enters through the front door.", speed)
                story_continuation = "Jack entered through the front door and heard a creaking noise. He saw shadows moving in the hallway."

            speak(tts_service, story_continuation, speed)

            # Second Interactive Question
            speak(tts_service, "Should Jack read the diary or explore the house further?", speed)
            choice2 = raw_input("Enter 1 to read the diary or 2 to explore the house: ")

            if choice2 == '1':
                speak(tts_service, "Jack read the diary and learned about the house's history. Suddenly, he felt a cold breeze and saw a ghostly figure approaching.", speed)
            elif choice2 == '2':
                speak(tts_service, "Jack continued exploring and found a hidden staircase leading to the basement. He heard whispers and felt a presence behind him.", speed)
            else:
                speak(tts_service, "Sorry, I didn't understand your choice. Let's assume Jack reads the diary.", speed)
                speak(tts_service, "Jack read the diary and learned about the house's history. Suddenly, he felt a cold breeze and saw a ghostly figure approaching.", speed)

            speak(tts_service, "The end. I hope you enjoyed the story!", speed)

            speak(tts_service, 'Bye bye, see you next time!!', speed)
            wave_hello(motion_service)

        elif val == 'not scared':
            speak(tts_service, 'since the last time you were not scared about my story, now I will tell you a more scary one', speed)

            # Initial Story
            speak(tts_service, "Once upon a time, in a friendly forest, there was a little bunny named Bubbles. Bubbles loved to hop around and make new friends. One day, Bubbles found a shiny, magical flower.", speed)

            # First Interactive Question
            speak(tts_service, "What should Bubbles do with the flower? Should Bubbles pick it up or leave it?", speed)
            choice1 = raw_input("Enter 1 to pick it up or 2 to leave it: ")

            if choice1 == '1':
                speak(tts_service, "Bubbles picked up the flower and suddenly, a rainbow appeared in the sky! Bubbles was excited and decided to follow the rainbow.", speed)
                story_continuation = "Bubbles and Squeaky decided to explore the forest together. They heard a soft music coming from the bushes."
            elif choice1 == '2':
                speak(tts_service, "Bubbles left the flower and continued hopping around. Soon, Bubbles found a friendly squirrel named Squeaky who wanted to play.", speed)
                story_continuation = "Bubbles and Squeaky decided to explore the forest together. They heard a soft music coming from the bushes."
            else:
                speak(tts_service, "Sorry, I didn't understand your choice. Let's assume Bubbles picks up the flower.", speed)
                story_continuation = "Bubbles picked up the flower and suddenly, a rainbow appeared in the sky! Bubbles was excited and decided to follow the rainbow."

            speak(tts_service, story_continuation, speed)

            # Second Interactive Question
            speak(tts_service, "Should Bubbles and Squeaky follow the music or continue exploring?", speed)
            choice2 = raw_input("Enter 1 to follow the music or 2 to continue exploring: ")

            if choice2 == '1':
                speak(tts_service, "They followed the music and found a group of fairies having a picnic. The fairies invited them to join and they all had a wonderful time.", speed)
            elif choice2 == '2':
                speak(tts_service, "They continued exploring and found a hidden pond with colorful fish. They played by the pond and enjoyed the beautiful day.", speed)
            else:
                speak(tts_service, "Sorry, I didn't understand your choice. Let's assume they continue exploring.", speed)
                speak(tts_service, "They continued exploring and found a hidden pond with colorful fish. They played by the pond and enjoyed the beautiful day.", speed)

            speak(tts_service, "The end. I hope you enjoyed the story!", speed)

            speak(tts_service, 'Bye bye, see you next time!!', speed)
            wave_hello(motion_service)

if __name__ == "__main__":
    main()
