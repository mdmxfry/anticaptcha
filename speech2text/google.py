import re
import random

import speech_recognition as sr

from config import SUCCESS_RATE, NUM_OF_DIGITS, SIMILAR


def replace_similar_sound(word):
    """
    Replace similar sounding words with digits
    :param word:
    :return:
    """
    for (key, value) in SIMILAR.items():
        if word in value:
            return str(key)
    raise Exception('No similar sound was found')


def randomize_difference(digits, difference, just_one=True):
    """
    Adds digits that can't be retrieved from the wav
    :param digits:
    :param difference:
    :param just_one:
    :return:
    """
    if just_one:
        insert = lambda: str(1)
    else:
        insert = lambda: str(random.randint(0, 9))
    for i in range(difference):
        digits.append(insert())
    return ''.join(digits), (SUCCESS_RATE ** len(digits)) * (0.1 ** difference)


def recognize_google(filename):
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio = r.record(source)

    response = r.recognize_google(audio)
    if response is not None:
        return post_process(response)


def post_process(result):
    """
    Filter all whitespaces,
    Convert words if any of them are digits
    Fill with ones if not enough digits

    :param result:
    :return:
    """
    result = result.replace(' ', '')

    digits = re.findall('(\d)', result)
    words = re.findall('(\D+)', result)
    if digits:
        if len(digits) == NUM_OF_DIGITS:
            return ''.join(digits), SUCCESS_RATE ** len(digits)
        elif len(digits) < NUM_OF_DIGITS and words:
            try:
                digits_from_words = [replace_similar_sound(word) for word in words]
                for (i, (word, digit)) in enumerate(zip(words, digits_from_words)):
                    if digit:
                        digits.insert(result.index(word), digit)
                        result = result.replace(word, digit)
                return ''.join(digits), SUCCESS_RATE ** len(digits)
            except Exception:
                pass
    return randomize_difference(digits, NUM_OF_DIGITS - len(digits))