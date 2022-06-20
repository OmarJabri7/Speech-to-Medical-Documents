from google.cloud import speech_v1 as speech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../data/euro-med-353820-86d6bbeb25fd.json"

def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    print_sentences(response)


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        print("-" * 80)
        print(f"Transcript: {transcript}")
        print(f"Confidence: {confidence:.0%}")


config = dict(language_code="en-US")
audio = dict(uri="gs://cloud-samples-data/speech/brooklyn_bridge.flac")

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
            # try:
            audio = recognizer.listen(source)
            command = speech_to_text(config, audio)
            print(command)
            # except:
            #     engine.say("Please say that again")
            #     engine.runAndWait()
            #     command = ""
            #     pass
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

