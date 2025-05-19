import sounddevice as sd
import numpy as np
import wave
import os
from scipy import signal
import tempfile
import time

def record_sample(duration=5, sample_rate=16000):
    """Record an audio sample."""
    print(f"\nRecording for {duration} seconds...")
    print("Speak now!")
    
    # Record audio
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )
    sd.wait()
    return recording.flatten()

def save_voice_signature(samples, output_path):
    """Process and save voice signature."""
    # Average the samples
    avg_sample = np.mean(samples, axis=0)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save signature
    np.save(output_path, avg_sample)
    return True

def main():
    print("Voice Registration Process")
    print("=========================")
    print("We'll record 3 samples of your voice.")
    print("Please speak the phrase: 'Voice authentication test'")
    
    samples = []
    
    for i in range(3):
        input(f"\nPress Enter to start recording sample {i+1}/3...")
        print("Starting in:")
        for count in range(3, 0, -1):
            print(count)
            time.sleep(1)
            
        try:
            sample = record_sample()
            samples.append(sample)
            print("Sample recorded successfully!")
        except Exception as e:
            print(f"Error recording sample: {str(e)}")
            return False
    
    # Save voice signature
    signature_path = os.path.join(
        os.path.dirname(__file__),
        'assistant',
        'voice_signature.npy'
    )
    
    if save_voice_signature(samples, signature_path):
        print("\nVoice registration successful!")
        print(f"Signature saved to: {signature_path}")
        return True
    else:
        print("\nError saving voice signature.")
        return False

if __name__ == "__main__":
    main()