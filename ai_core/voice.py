import speech_recognition as sr
import os
import sys
import threading
import queue

# Try importing Coqui TTS for realistic voice
try:
    from TTS.api import TTS
    HAS_COQUI = True
except ImportError:
    HAS_COQUI = False

# Fallback TTS
import pyttsx3

class VoiceInterface:
    def __init__(self, use_coqui=False, model_name="tts_models/en/ljspeech/glow-tts"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.use_coqui = use_coqui and HAS_COQUI
        
        # Initialize TTS
        if self.use_coqui:
            print(f"Initializing Coqui TTS with model: {model_name}...")
            # This might take a while to download on first run
            self.tts_engine = TTS(model_name=model_name, progress_bar=False, gpu=False)
        else:
            print("Initializing System TTS (pyttsx3)...")
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)

    def listen(self, timeout=5):
        """
        Listens to the microphone and returns the recognized text.
        """
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                print("Processing audio...")
                # Using Google Web Speech API for better accuracy out-of-the-box without large local models
                # For purely local, one would switch to recognizer.recognize_whisper(audio)
                text = self.recognizer.recognize_google(audio)
                print(f"Heard: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

    def speak(self, text):
        """
        Speaks the given text using the configured TTS engine.
        """
        print(f"Speaking: {text}")
        if self.use_coqui:
            # Coqui TTS output to file and play (simplified)
            # In a real app, we'd stream this or use a better player
            output_file = "/tmp/echoos_speech.wav"
            self.tts_engine.tts_to_file(text=text, file_path=output_file)
            if sys.platform == "linux":
                os.system(f"aplay {output_file}")
            elif sys.platform == "darwin":
                os.system(f"afplay {output_file}")
            # Windows play sound not implemented in this snippet for Coqui
        else:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

if __name__ == "__main__":
    # Test the interface
    voice = VoiceInterface(use_coqui=False) # Set True if you have Coqui installed
    voice.speak("Hello, I am Echo OS. I am ready to serve you.")
    
    print("Say something...")
    heard = voice.listen()
    if heard:
        voice.speak(f"You said: {heard}")
