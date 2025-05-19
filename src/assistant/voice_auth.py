import numpy as np
from scipy import signal
import os

class VoiceAuthenticator:
    def __init__(self, threshold=0.5):  # Lowered threshold
        self.voice_signature = None
        self.signature_path = os.path.join(os.path.dirname(__file__), 'voice_signature.npy')
        self.threshold = threshold
        self.load_voice_signature()
        
    def load_voice_signature(self):
        try:
            self.voice_signature = np.load(self.signature_path)
            print(f"Loaded voice signature with length: {len(self.voice_signature)}")
        except FileNotFoundError:
            print("No voice signature found. Please register your voice first.")
            
    def verify_voice(self, audio):
        try:
            # Convert audio to numpy array
            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
            print(f"Input audio length: {len(audio_data)}")
            
            if self.voice_signature is None:
                return True
            
            # Normalize audio data
            audio_data = audio_data / np.max(np.abs(audio_data))
            signature = self.voice_signature / np.max(np.abs(self.voice_signature))
            
            # Use multiple features for comparison
            correlations = []
            
            # Time domain correlation
            min_length = min(len(audio_data), len(signature))
            time_corr = np.corrcoef(
                audio_data[:min_length],
                signature[:min_length]
            )[0, 1]
            correlations.append(time_corr)
            
            # Frequency domain correlation
            _, _, audio_spec = signal.spectrogram(
                audio_data, 
                fs=16000, 
                nperseg=256, 
                noverlap=128,
                window='hann'
            )
            _, _, sig_spec = signal.spectrogram(
                signature, 
                fs=16000, 
                nperseg=256, 
                noverlap=128,
                window='hann'
            )
            
            # Match spectrogram sizes
            min_time = min(audio_spec.shape[1], sig_spec.shape[1])
            freq_corr = np.corrcoef(
                audio_spec[:, :min_time].flatten(),
                sig_spec[:, :min_time].flatten()
            )[0, 1]
            correlations.append(freq_corr)
            
            # Calculate final score
            final_score = np.mean(correlations)
            print(f"Voice correlations - Time: {time_corr:.2f}, Freq: {freq_corr:.2f}")
            print(f"Final score: {final_score:.2f} (threshold: {self.threshold})")
            
            return final_score > self.threshold
            
        except Exception as e:
            print(f"Voice verification error: {str(e)}")
            return False