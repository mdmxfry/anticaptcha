import os
import urllib.request

from speech2text.google import recognize_google
from speech2text.watson import recognize as recognize_ibm
from speech2text.watson import recognize_with_text as recognize_ibm_text

from config import AUDIO_STARTS


CWD = os.getcwd()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(CWD, 'credits/google_creds.json')
os.environ['WATSON_APPLICATION_CREDENTIALS'] = os.path.join(CWD, 'credits/watson_creds.json')


def download_and_recognize(url, download_location, watson=False, auto_remove=True, text=False):
    """
    Entry point function.
    :param url: MP3 Url
    :param download_location: Path to store files
    :param watson: Default: False. True if you want to use Watson Speech Recognition, False otherwise
    :param auto_remove: Default: True. Remove files after recognition
    :param text: Default: False. This is Watson only parameter, to use text recognition, not only digits
    :return:
    """
    filename = str(hash(url)) + '.mp3'
    full_path_mp3 = os.path.join(os.getcwd(), download_location, filename)

    if watson and text:
        new_full_path = full_path_mp3
    elif watson:
        new_full_path = full_path_mp3[:-4] + '_trunc' + '.mp3'
    else:
        new_full_path = full_path_mp3[:-4] + '.wav'

    urllib.request.urlretrieve(url, full_path_mp3)

    # Convert the file to a format our APIs will understand using ffmpeg
    cmd = 'echo \'y\' | ffmpeg -ss {} -i {} {} 2>/dev/null'.format(AUDIO_STARTS, full_path_mp3, new_full_path)
    if not text:
        os.system(cmd)

    assert os.path.exists(new_full_path)

    if watson and text:
        response = recognize_ibm_text(new_full_path)
    elif watson:
        response = recognize_ibm(new_full_path)
    else:
        response = recognize_google(new_full_path)

    if auto_remove:
        os.system('rm {} {}'.format(full_path_mp3, new_full_path))

    return response
