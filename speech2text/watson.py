import os
import json

from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import WatsonApiException
from watson_developer_cloud.websocket import RecognizeCallback

credentials_path = os.environ.get('WATSON_APPLICATION_CREDENTIALS')

with open(credentials_path, 'r') as file:
    creds = json.loads(file.read())

SPEECH_TO_TEXT_APIKEY = creds['apikey']
SPEECH_TO_TEXT_URL = creds['url']

speech_to_text = SpeechToTextV1(
    iam_apikey=SPEECH_TO_TEXT_APIKEY,
    url=SPEECH_TO_TEXT_URL
)

digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0'
}


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        return json.loads(data, indent=2)

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))


myRecognizeCallback = MyRecognizeCallback()


def post_process(response):
    resp_digits = response.result['results'][0]['alternatives'][0]['transcript']
    confidence = response.result['results'][0]['alternatives'][0]['confidence']

    int_digits = []
    for digit in resp_digits.split(' '):
        if digit in digits.keys():
            int_digits.append(digits[digit])
        else:
            int_digits.append(digit)

    return ''.join(int_digits), confidence


def post_process_text(response):
    resp_text = response.result['results'][0]['alternatives'][0]['transcript']
    confidence = response.result['results'][0]['alternatives'][0]['confidence']
    return resp_text.strip(), confidence


def recognize(filename):
    try:
        print('Recognizing: {}'.format(filename))
        with open(os.path.join(filename), 'rb') as audio_file:
            response = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/mp3',
                model='en-US_BroadbandModel',
                keywords=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero'],
                keywords_threshold=0.5,
                max_alternatives=1)
            return post_process(response)
    except WatsonApiException as ex:
        print('Method failed with status code ' + str(ex.code) + ': ' + ex.message)


def recognize_with_text(filename):
    try:
        print('Recognizing: {}'.format(filename))
        with open(os.path.join(filename), 'rb') as audio_file:
            response = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/mp3',
                model='en-US_BroadbandModel',
                max_alternatives=1)
            return post_process_text(response)
    except WatsonApiException as ex:
        print('Method failed with status code ' + str(ex.code) + ': ' + ex.message)
