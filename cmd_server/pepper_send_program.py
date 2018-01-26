#!/usr/bin/env python

import sys
import os
import socket
import importlib
import re
import argparse
import qi


def start_client(server_ip,server_port,program):

    TCP_IP = ''
    BUFFER_SIZE = 200

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((server_ip,server_port))

    f = open(program,'r') 
    data = f.read() 
    f.close()

    s.send(data)

    s.close()

    print("Closed connection")




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", type=str, default='127.0.0.1',
                        help="Server IP address.")
    parser.add_argument("--serverport", type=int, default=5000,
                        help="Server port")
    parser.add_argument("--program", type=str, default="default.py",
                        help="Program file to send")

    args = parser.parse_args()
    server_ip = args.serverip
    server_port = args.serverport 
    program = args.program

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Send program", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    pepper_cmd.session = app.session

    start_client(server_ip,server_port,program)
    


if __name__ == "__main__":
    main()


