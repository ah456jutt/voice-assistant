import sounddevice as sd
import numpy as np
import wave
import threading
import queue
import tempfile
import os

class AudioHandler:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
    def callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        self.audio_queue.put(indata.copy())
        
    def record_audio(self, duration=5):
        self.audio_queue = queue.Queue()
        self.is_recording = True
        
        with sd.InputStream(samplerate=self.sample_rate,
                          channels=1,
                          callback=self.callback):
            temp_file = tempfile.mktemp(suffix=".wav")
            audio_data = []
            
            print("Recording...")
            sd.sleep(int(duration * 1000))
            
            while not self.audio_queue.empty():
                audio_data.append(self.audio_queue.get())
                
            audio_data = np.concatenate(audio_data, axis=0)
            
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            
            return temp_file