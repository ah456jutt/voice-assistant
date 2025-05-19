import speech_recognition as sr
import pyttsx3
import random
import sounddevice as sd
import numpy as np
import wave
import io
from assistant.task_manager import TaskManager

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        
        # Set female voice by default
        for voice in self.voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Increase speech rate for faster response
        self.engine.setProperty('rate', 175)
        
        self.recognizer = sr.Recognizer()
        self.task_manager = TaskManager()
        self.sample_rate = 16000
        self.channels = 1
        
        # Configure sounddevice
        sd.default.samplerate = self.sample_rate
        sd.default.channels = self.channels

        self.mode = None  # Will be set based on user choice

    def speak(self, text):
        # Split the text if it contains "Command output:"
        if "Command output:" in text:
            print(f"Assistant: {text}")  # Print full message with prefix
            # Only speak the actual output part
            output_text = text.split("Command output:")[1].strip()
            self.engine.say(output_text)
        else:
            # For non-command outputs, both print and speak
            print(f"Assistant: {text}")
            self.engine.say(text)
    
        self.engine.runAndWait()

    def listen(self):
        try:
            print("\nListening...")
            
            # Adjust audio settings
            chunks = []
            silence_count = 0
            max_silence = 8  # Increased from 4 to 8 for better detection
            min_volume = 0.01  # Reduced threshold for better sensitivity
            
            def callback(indata, frames, time, status):
                if status:
                    print(f"Debug - Audio status: {status}")
                    return
                
                volume_norm = np.linalg.norm(indata) / frames
                if volume_norm < min_volume:
                    nonlocal silence_count
                    silence_count += 1
                else:
                    silence_count = 0
                chunks.append(indata.copy())

            # Configure input stream with better settings
            with sd.InputStream(
                callback=callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=int(self.sample_rate * 0.25),  # Reduced chunk size
                device=None,  # Use default device
                dtype=np.float32,
                latency='high',  # More stable latency
                extra_settings=None
            ):
                print("Go ahead, I'm listening...")
                while silence_count < max_silence:
                    sd.sleep(250)  # Reduced sleep time for better responsiveness
            
            if chunks and len(chunks) > 2:  # Ensure we have enough audio data
                audio_data = np.concatenate(chunks, axis=0)
                audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
                
                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wav:
                    wav.setnchannels(self.channels)
                    wav.setsampwidth(2)
                    wav.setframerate(self.sample_rate)
                    wav.writeframes(audio_data.tobytes())
                
                return sr.AudioData(wav_buffer.getvalue(), self.sample_rate, 2)
            
            print("No speech detected")
            return None
            
        except Exception as e:
            print(f"Debug - Recording error: {str(e)}")
            return None

    def recognize_speech(self, audio):
        try:
            text = self.recognizer.recognize_google(audio).lower()
            if text:
                print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            self.speak("Sorry, I'm having trouble accessing the speech service.")
            return None

    def handle_command(self, command):
        return self.task_manager.handle_command(command)

    def text_mode(self):
        self.speak("Text mode activated. Type your commands (type 'exit' to quit)")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                print("-" * 50)
                
                if command == "exit" or command == "goodbye":
                    self.speak("Goodbye!")
                    break
                    
                response = self.handle_command(command)
                if response:
                    self.speak(response)
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                self.speak("Sorry, I encountered an error. Please try again.")

    def voice_mode(self):
        self.speak("Voice mode activated. Say your commands (say 'exit' or 'goodbye' to quit)")
        while True:
            try:
                audio = self.listen()
                if audio is None:
                    self.speak("Sorry, I didn't catch that. Please try again.")
                    continue

                command = self.recognize_speech(audio)
                if not command:
                    continue

                if command in ["exit", "goodbye"]:
                    self.speak("Goodbye!")
                    break

                response = self.handle_command(command)
                if response:
                    self.speak(response)

            except Exception as e:
                print(f"Error: {str(e)}")
                self.speak("Sorry, I encountered an error. Please try again.")

    def run(self):
        self.speak("Welcome to Voice Assistant!")
        self.mode = self.select_mode()
        
        if self.mode == "voice":
            self.voice_mode()
        else:
            self.text_mode()

    def select_mode(self):
        print("\n=== Voice Assistant Mode Selection ===")
        print("1. Voice Mode (Speech recognition)")
        print("2. Text Mode (Type commands)")
        
        while True:
            try:
                choice = input("\nSelect mode (1 or 2): ").strip()
                if choice == "1":
                    return "voice"
                elif choice == "2":
                    return "text"
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()