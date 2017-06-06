import os
import urllib
import requests
import json
import slu_utils


class GoogleClient:
    timeout = 10000
    url = ''
    headers = {"Content-Type": "audio/x-flac; rate=16000"}

    def __init__(self, language, key_file):
        keys = slu_utils.lines_to_list(key_file)
        q = {"output": "json", "lang": language, "key": keys[0]}
        self.url = "https://www.google.com/speech-api/v2/recognize?%s" % (urllib.urlencode(q))

    def recognize_file(self, file_path):
        try:
            print '[GOOGLE] Recognizing..'
            transcriptions = []
            data = open(file_path, "rb").read()
            response = requests.post(self.url, headers=self.headers, data=data, timeout=self.timeout)
            json_units = response.text.split(os.linesep)
            print json_units
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
        except ValueError as ve:
            print '[RECOGNIZE]ERROR! Google APIs are temporary unavailable. Returning empty list..'
            return []
        except requests.exceptions.RequestException as e:
            print e
            print '[RECOGNIZE]ERROR! Unable to reach Google. Returning empty list..'
            return []

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
        except ValueError as ve:
            print '[RECOGNIZE]ERROR! Google APIs are temporary unavailable. Returning empty list..'
            return []
        except requests.exceptions.RequestException as e:
            print e
            print '[RECOGNIZE]ERROR! Unable to reach Google. Returning empty list..'
            return []


def main():
    g = GoogleClient("en-US", "google_keys.txt")
    while True:
        print g.recognize_file('file.flac')


if __name__ == "__main__":
    main()
