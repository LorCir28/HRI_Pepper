import argparse
import json
from lu4r.client import LU4RClient

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--pip", type=str, default="127.0.0.1",
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
	parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
	parser.add_argument("--lip", type=str, default="127.0.0.1",
                        help="LU4R IP address.")
	parser.add_argument("--lport", type=int, default="9001",
                        help="LU4R listening port.")
	args = parser.parse_args()
	pip = args.pip
	pport = args.pport
	lip = args.lip
	lport = args.lport
    
	client = LU4RClient(lip, lport)
	
	sentence = 'bring me the mug'
	sentences = ['move to the kitchen','bring me the mug','take the glass']
	print client.parse_sentence(sentence)
	print client.parse_sentences(sentences)
    
    #state = args.state

    #Start working session
    #session = qi.Session()
    #try:
    #    session.connect("tcp://" + pip + ":" + str(pport))
    #except RuntimeError:
    #    print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
    #           "Please check your script arguments. Run with -h option for help.")
    #    sys.exit(1)


    #tts_service = session.service("ALTextToSpeech")

if __name__ == "__main__":
	main()
