from gtts import gTTS
import os
from parser_func import get_info

def make_speech():
    mytext = str(get_info())
    language = 'ru'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    os.chdir('D:\\Python\\TG-galereya-bot\\voice\\')
    myobj.save(f'voice.ogg')
