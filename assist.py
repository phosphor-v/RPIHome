import speech_recognition as sr
import os
import pyttsx3
from voice_commands import commands
engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voices = [v for v in voices if v.gender == 'female']
if female_voices:
    engine.setProperty('voice', female_voices[1].id)
engine.setProperty('rate', 150)
# load the voice commands


# initialize the speech recognizer
r = sr.Recognizer()

# set the microphone as source
mic = sr.Microphone()

os.environ["ALSA_OUTPUT_DEVICE"] = "default"
def speak(text):
    engine.say(text)
    engine.runAndWait()
# main loop
speak("hello")
while True:
    with mic as source:
        # adjust the microphone sensitivity
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

        # recognize the wake word "assistant"
        try:
            wake_word = r.recognize_google(audio)
            print("You said:", wake_word)

            if "assistant" in wake_word.lower():
                speak("How can I help you?")
                audio = r.listen(source)

                # recognize speech using Google Speech Recognition
                try:
                    command = r.recognize_google(audio)
                    print("You said:", command)

                    # execute the command if recognized
                    if command.lower() in commands:
                        # execute the command and get the response
                        response = eval(commands[command.lower()])

                        speak(response)

                except sr.UnknownValueError:
                    speak("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
