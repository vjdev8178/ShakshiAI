import edge_tts
import asyncio
import pygame
import os

# Voice setting
VOICE = "en-US-AnaNeural" 
# Other options: "en-IN-NeerjaNeural" (Indian English)

async def _speak_async(text):
    """
    Ye internal function hai jo actual async kaam karega.
    """
    output_file = "temp_voice.mp3"
    
    # 1. Text to Audio conversion
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

    # 2. Audio playback setup
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        # Jab tak audio play ho raha hai wait karo
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"Error in playback: {e}")
        
    finally:
        # Cleanup
        pygame.mixer.quit()
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass

def speak(text):
    """
    Ye wo wrapper function hai jo tumhari ui.py file dhoond rahi hai.
    Ye async function ko synchronous tarike se run kar dega.
    """
    try:
        asyncio.run(_speak_async(text))
    except Exception as e:
        print(f"Speaking Error: {e}")

# Testing ke liye (Direct run karne par ye chalega)
if __name__ == "__main__":
    speak("Hello! The error is fixed now.")