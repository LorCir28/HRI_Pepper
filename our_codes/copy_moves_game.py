import qi
import argparse
import random
import sys
import time
import os


def perform_movements(motion_service, speed):
    # Define the joints for the head and arms
    head_movements = ["HeadYaw", "HeadPitch"]
    arm_movements = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                     "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    
    # Generate random angles for the head movements
    head_angles = [random.uniform(-0.5, 0.5) for _ in head_movements]
    # Generate random angles for the arm movements
    arm_angles = [random.uniform(-1.0, 1.0) for _ in arm_movements]
    
    # Perform head movements
    for i, joint in enumerate(head_movements):
        motion_service.angleInterpolation(joint, head_angles[i], [speed], True)
    
    # Perform arm movements
    for i, joint in enumerate(arm_movements):
        motion_service.angleInterpolation(joint, arm_angles[i], [speed], True)


def reset_to_initial_configuration(motion_service):
    # Define the initial configuration for the head and arm joints
    names = ["HeadYaw", "HeadPitch", 
             "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
             "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    angles = [0.0, 0.0, 
              1.5, 0.3, -1.2, -0.5, 0.0,
              1.5, -0.3, 1.2, 0.5, 0.0]  # Example neutral positions
    times = [1.0] * len(names)  # Time in seconds to reach the initial position
    
    # Move all joints to the initial configuration
    motion_service.angleInterpolation(names, angles, times, True)


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

    tts_service.say("Hello, What is your name?")
    user = raw_input("Please enter your name: ")

    try:
        # KNOWN USER
        known_user = memory_service.getData(user)
        tts_service.say("Hello" + " "  + known_user + ", I can recognize you!!")


    except:
        # UNKNOWN USER
        memory_service.insertData(user, user)
        tts_service.say('Hello' + ' ' + user + ', nice to meet you for the first time!!')

    tts_service.say("I'm gonna to propose to you a game!")
    tts_service.say("It's very simple: you have to copy my movements")
    tts_service.say("Let's begin!!")

    speed = 0.6 # pepper's movements speed

    n_attempts = 0

    while True:
        reset_to_initial_configuration(motion_service)
        perform_movements(motion_service, speed)
        reset_to_initial_configuration(motion_service)
        
        # Simulate user response (this is where you would integrate user feedback mechanisms)
        tts_service.say("Did you successfully follow the movements?: ")
        choice = raw_input("Enter 1 for 'yes' or 2 for 'no': ")

        # at most three attempts for the user
        n_attempts += 1
        if n_attempts == 3:
            break
        
        if choice == '1':
            tts_service.say("Great job! Let's speed up a bit.")
            speed -= 0.2
        else:
            tts_service.say("Oops! Let's slow down a bit.")
            speed += 0.2

        # Give a short break between rounds
        time.sleep(2)


    tts_service.say("Good job" + " " + user + "! See you soon!!")

    app.stop()



if __name__ == "__main__":
    main()