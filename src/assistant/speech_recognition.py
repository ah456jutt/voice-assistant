import speech_recognition as sr
from .audio_handler import AudioHandler
import os

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_handler = AudioHandler()
        
    def listen(self):
        print("Listening...")
        audio_file = self.audio_handler.record_audio(duration=5)
        
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            
        # Clean up temporary file
        os.remove(audio_file)
        return audio
    
    def recognize(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results")
            return None