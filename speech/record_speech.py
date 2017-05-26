import qi
import argparse
import sys
import time
import tempfile


def main(session):

	channels = [0,0,1,0] #Left, Right, Front, Rear
	audio_recorder = session.service("ALAudioRecorder")
	audio_player_service = session.service("ALAudioPlayer")
	filepath = "pepper_audio_prova"
	audio_recorder.startMicrophonesRecording(filepath, "wav", 48000, channels)
	time.sleep(10)
	audio_recorder.stopMicrophonesRecording()
	fileId = audio_player_service.loadFile(filepath)
	print fileId
	audio_player_service.play(fileId, _async=True)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--pip", type=str, default="127.0.0.1", help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--pport", type=int, default=9559, help="Naoqi port number")

	args = parser.parse_args()
	session = qi.Session()
	try:
		session.connect("tcp://" + args.pip + ":" + str(args.pport))
	except RuntimeError:
		print ("Can't connect to Naoqi at ip \"" + args.pip + "\" on port " + str(args.pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
		sys.exit(1)
	main(session)