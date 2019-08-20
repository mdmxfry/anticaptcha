# speech2text
Speech2Text for GeeTest captcha

```
pip3 install requirements.txt
```

## How to use
0. Select between Watson 

1. Write simple url finder with selenium/bs4. Url should lead to the .mp3 download.

2. Use this url to get the results

```
    url_to_mp3 = 'https://www.google.com/recaptcha/api2/payload?p=06AOLTBLRwWGROwb_oVh4JYXz3Bg558dIZH4oKrlfhzOY2-UV_lClcOF6BMeks_ZMMhhpW47JH92zI7u5WcchFi9QmNqnZfXOJSO_neAI_zxgCYAeSKwmtnhZ-rP926-leEqP-u2XVqS3lo4h3hdGkV0XfeJSgdTmuFw6CStkYAgIOBDHVnVpcyUY&k=6LfW6wATAAAAAHLqO2pb8bDBahxlMxNdo9g947u9'
    print(speech2text.download_and_recognize(url_to_mp3, 'files', watson=True, auto_remove=True, text=True))

```