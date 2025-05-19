import os
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
import numpy as np

class VoiceCloner:
    def __init__(self):
        self.voice_samples_dir = os.path.join(os.path.dirname(__file__), 'voice_samples')
        self.voice_file = os.path.join(self.voice_samples_dir, 'voice_sample.wav')
        os.makedirs(self.voice_samples_dir, exist_ok=True)

    def save_voice_sample(self, audio_data, sample_rate=24000):
        """Save a voice sample for cloning"""
        try:
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]
            
            # Normalize audio
            audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Save as WAV
            sf.write(self.voice_file, audio_data, sample_rate)
            return True
        except Exception as e:
            print(f"Error saving voice sample: {str(e)}")
            return False

    def generate_speech(self, text):
        """Generate speech using gTTS"""
        try:
            # Generate temporary file path
            temp_file = os.path.join(self.voice_samples_dir, 'temp_speech.mp3')
            
            # Generate speech using gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(temp_file)
            
            # Load the generated audio
            audio_data, sample_rate = sf.read(temp_file)
            
            # Clean up temporary file
            os.remove(temp_file)
            
            return audio_data

        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None