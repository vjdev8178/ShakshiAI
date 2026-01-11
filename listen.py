import speech_recognition as sr

def listen_audio():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        
        # Shor-sharaba adjust karne ke liye (Ambient Noise)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # 5 second tak wait karega ki tu kuch bole
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Recognizing...")
            # Google ki free speech API use kar rahe hain
            text = recognizer.recognize_google(audio, language='en-IN')
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Mic Error: {e}")
            return None

# Test karne ke liye (Run karke kuch bolna)
if __name__ == "__main__":
    print(listen_audio())