import qi
import argparse
import json
import sys
from google.client import ASRClient

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--pip", type=str, default="127.0.0.1",
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
	args = parser.parse_args()
	pip = args.pip
	pport = args.pport

	#Start working session
	session = qi.Session()
	try:
		session.connect("tcp://" + pip + ":" + str(pport))
		print 'Connected'
	except RuntimeError:
		print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
			   "Please check your script arguments. Run with -h option for help.")
		sys.exit(1)

	#AIzaSyAONQ_K4NOIGfRWXmiuXonThf2rs3XzKPY
	#AIzaSyDya-9naDiG0Dm8MVVKhQw50HmsvfZeZfE
	client = ASRClient('en-US', 'AIzaSyDya-9naDiG0Dm8MVVKhQw50HmsvfZeZfE')

	filepath = 'File16.wav'
	
	print client.recognize(filepath)

if __name__ == "__main__":
	main()
