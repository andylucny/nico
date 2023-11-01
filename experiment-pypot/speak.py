import pyttsx3
from agentspace import space

def speak(text, language='en', unconditional=False):
    if not unconditional:
        if not space(default=False)['TellIstructions']:
            print('speaking avoided')
            return
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    speaker = 3 if language == 'sk' else 2 # 3 is slovak Filip, 0 is David, 1 Markus, 2 Hazel
    engine.setProperty('voice', voices[speaker].id)
    engine.say(text)
    print('speaking on <'+text+'>')
    engine.runAndWait()
    print('speaking off')

if __name__ == "__main__":
    speak('preparing, please, wait')
    print('done')
