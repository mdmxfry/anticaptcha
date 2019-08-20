from speech2text import speech2text

from config import FILES_PATH


if __name__ == '__main__':
    # Get URL from page where Recaptcha/Geetest was found
    url_to_mp3 = 'https://www.google.com/recaptcha/api2/payload?p=06AOLTBLRwWGROwb_oVh4JYXz3Bg558dIZH4oKrlfhzOY2-UV_lClcOF6BMeks_ZMMhhpW47JH92zI7u5WcchFi9QmNqnZfXOJSO_neAI_zxgCYAeSKwmtnhZ-rP926-leEqP-u2XVqS3lo4h3hdGkV0XfeJSgdTmuFw6CStkYAgIOBDHVnVpcyUY&k=6LfW6wATAAAAAHLqO2pb8bDBahxlMxNdo9g947u9'

    # Google Speech Recognition Example
    print(speech2text.download_and_recognize(url_to_mp3, FILES_PATH, auto_remove=True, text=True))

    # Watson Speech Recognition Example
    print(speech2text.download_and_recognize(url_to_mp3, FILES_PATH, watson=True, auto_remove=True, text=True))