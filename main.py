from brain import ask_ai
from speak import speak  # <--- Ye humne import kiya

print("🤖 Shakshi is Online... (Bolne ke liye taiyaar)")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "bye", "quit"]:
        speak("Bye Vijay, take care.")
        print("Shakshi: Bye Vijay, take care.")
        break
    
    # 1. AI se jawaab maanga
    reply = ask_ai(user_input)
    
    # 2. Jawaab print kiya
    print(f"Shakshi: {reply}")
    
    # 3. Ab Shakshi bolegi 🗣️
    speak(reply)