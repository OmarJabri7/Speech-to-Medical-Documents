import pyttsx3
import speech_recognition as sr
import numpy as np
recognizer = sr.Recognizer()
# recognizer.energy_threshold = 100
microphone = sr.Microphone()
text_data = []
engine = pyttsx3.init()
engine.say("Recording")
engine.runAndWait()
print("Recording....")
interrupt = False
while True:
    try:
        if interrupt: break
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
            except:
                engine.say("Please say that again")
                engine.runAndWait()
                command = ""
                pass
            print(command)
            if "euro-med".lower() in command.lower():
                try:
                    while True:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        print(command)
                        text_data.append(command)
                except KeyboardInterrupt:
                    interrupt = True
                    break
    except:
        pass
print("Finished Record")
with open("doctor_notes.txt", "w") as outfile:
    outfile.write("\n".join(text_data))
