import pyttsx3

def speak(text, language='sk'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    speaker = 3 if language == 'sk' else 2 # 3 is slovak Filip, 0 is David, 1 Markus, 2 Hazel
    engine.setProperty('voice', voices[speaker].id)
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')
