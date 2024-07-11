import qi
import argparse
import sys
import time
import os


# user = 'Camilla'
user = 'Claudio'
# user = 'Lorenzo'


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
    parser.add_argument("--pip", type=str, default='127.0.0.1',
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
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

    # Starting application
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

    try:
        val = memory_service.getData(user)
        strsay = 'Hello' + ' ' + user + ', I can recognize you!!'
    except:
        memory_service.insertData(user, user)
        strsay = 'Hello' + ' ' + user + ', nice to meet you for the first time!!'
        
    tts_service.say(strsay)
    tts_service.say(strsay)
    wave_hello(motion_service)
    print("  -- Say: " + strsay)

    # Keep the application running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping application")
        app.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()


