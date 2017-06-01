import os
import urllib
import requests
import json


class GoogleClient:
    timeout = 10000
    url = ''
    headers = {"Content-Type": "audio/x-flac; rate=16000"}

    def __init__(self, language, key_file):
        keys = self.read_google_keys(key_file)
        print keys
        q = {"output": "json", "lang": language, "key": keys[0]}
        self.url = "http://www.google.com/speech-api/v2/recognize?%s" % (urllib.urlencode(q))

    def read_google_keys(self, key_file):
        with open(key_file) as f:
            keys = f.readlines()
        return [x.strip() for x in keys]

    def recognize_file(self, file_path):
        try:
            print '[GOOGLE] Recognizing..'
            transcriptions = []
            data = open(file_path, "rb").read()
            response = requests.post(self.url, headers=self.headers, data=data, timeout=self.timeout)
            json_units = response.text.split(os.linesep)
            for unit in json_units:
                if not unit:
                    continue
                obj = json.loads(unit)
                alternatives = obj["result"]
                if len(alternatives) > 0:
                    for obj in alternatives:
                        results = obj["alternative"]
                        for result in results:
                            transcriptions.append(result["transcript"])
            return transcriptions
        except requests.exceptions.RequestException as e:
            print e
            print '[RECOGNIZE]ERROR! Unable to reach Google.'
            return 0

    def recognize_data(self, data):
        try:
            print '[GOOGLE] Recognizing..'
            transcriptions = []
            response = requests.post(self.url, headers=self.headers, data=data, timeout=self.timeout)
            json_units = response.text.split(os.linesep)
            for unit in json_units:
                if not unit:
                    continue
                obj = json.loads(unit)
                alternatives = obj["result"]
                if len(alternatives) > 0:
                    for obj in alternatives:
                        results = obj["alternative"]
                        for result in results:
                            transcriptions.append(result["transcript"])
            return transcriptions
        except requests.exceptions.RequestException as e:
            print e
            print '[RECOGNIZE]ERROR! Unable to reach Google.'
            return 0
