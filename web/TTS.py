from gtts import gTTS
from .models import Fach, LernSet, LernKarte, Progress

def test_button():
    mytext = 'Hallo! Mein Name ist Metis und ich bin dein virtueller Lernassistent'
    language = 'de'
    tts = gTTS(text=mytext, lang=language, slow=False)
    tts.save('testbegrüssung.mp3')

def say(requestUserId, cardId):
    karte = LernKarte.objects.get(id=cardId)
    sprache1 = karte.lernset.languageOne
    sprache2 = karte.lernset.languageTwo
    text1 = karte.txt_front
    text2 = karte.txt_back
    language = ''
    if sprache2 == 'EN':
        language = 'en'
    elif sprache2 == 'DE':
        language = 'de'
    elif sprache2 == 'FR':
        language = 'fr'
    mytext = text2
    tts = gTTS(text=mytext, lang=language, slow=False)
    name = str(requestUserId)
    name += '.mp3'
    tts.save(name)



