import customtkinter as ctk
import threading
import time
from brain import ask_ai
from speak import speak
from listen import listen_audio

# --- Theme Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # Blue theme for Jarvis look

class ShakshiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("SHAKSHI AI | SYSTEM DASHBOARD")
        self.geometry("900x600")
        
        # Grid Layout (1x2): Left Sidebar (Small) | Right Main Area (Big)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= LEFT SIDEBAR (Menu) =================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SHAKSHI AI\nVER 2.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Status Indicator (The Arc Reactor)
        self.status_btn = ctk.CTkButton(self.sidebar_frame, text="ONLINE", fg_color="#00FF00", hover=False, height=30, corner_radius=20)
        self.status_btn.grid(row=1, column=0, padx=20, pady=10)

        # Action Buttons
        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="Clear Chat", command=self.clear_chat, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clear_btn.grid(row=2, column=0, padx=20, pady=10)

        # Toggle Voice Mode (Dummy Switch for visuals)
        self.voice_switch = ctk.CTkSwitch(self.sidebar_frame, text="Always Listen")
        self.voice_switch.grid(row=3, column=0, padx=20, pady=10)

        # Footer
        self.footer_label = ctk.CTkLabel(self.sidebar_frame, text="System: Stable\nDev: Vijay", font=ctk.CTkFont(size=12))
        self.footer_label.grid(row=5, column=0, padx=20, pady=20)


        # ================= RIGHT MAIN AREA (Chat) =================
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Chat Display (Glassmorphismish look)
        self.chat_display = ctk.CTkTextbox(
            self.main_frame, 
            font=("Consolas", 16), # Modern Coding Font
            text_color="#E0E0E0",
            fg_color="#1a1a1a",     # Darker background
            corner_radius=15,
            border_width=1,
            border_color="#333333"
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        self.chat_display.insert("0.0", ">> SYSTEM INITIALIZED...\n>> WAITING FOR COMMAND.\n\n")
        self.chat_display.configure(state="disabled")


        # ================= BOTTOM INPUT AREA =================
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Mic Button (Stylized)
        self.mic_button = ctk.CTkButton(
            self.input_frame, 
            text="🎙", 
            width=50, 
            height=50, 
            font=("Arial", 24), 
            corner_radius=25, 
            fg_color="#1f6aa5", 
            hover_color="#144870",
            command=self.start_listening_thread
        )
        self.mic_button.grid(row=0, column=0, padx=(0, 10))

        # Text Entry (Floating Bar)
        self.user_input = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Type your command here...", 
            height=50, 
            font=("Roboto Medium", 14), 
            corner_radius=25,
            border_width=2,
            border_color="#333333"
        )
        self.user_input.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message_event)

        # Send Button (Arrow)
        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="➤", 
            width=60, 
            height=50, 
            font=("Arial", 20), 
            corner_radius=25, 
            fg_color="#00ADB5", # Cyber Cyan
            hover_color="#00797E",
            command=self.send_message
        )
        self.send_button.grid(row=0, column=2)

    # --- FUNCTIONS ---

    def change_status(self, status):
        # Sidebar wala status button color change karega
        if status == "thinking":
            self.status_btn.configure(fg_color="#FFD700", text="THINKING") # Gold
        elif status == "speaking":
            self.status_btn.configure(fg_color="#FF4500", text="SPEAKING") # Orange/Red
        elif status == "listening":
            self.status_btn.configure(fg_color="#00BFFF", text="LISTENING") # Deep Sky Blue
        else:
            self.status_btn.configure(fg_color="#00FF00", text="ONLINE") # Green

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.insert("0.0", ">> MEMORY CLEARED.\n\n")
        self.chat_display.configure(state="disabled")

    def typewriter_effect(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\n🤖 Shakshi: ")
        self.chat_display.see("end")
        
        for char in text:
            self.chat_display.insert("end", char)
            self.chat_display.see("end")
            self.update()
            time.sleep(0.01) # Typing speed fast rakhi hai
            
        self.chat_display.insert("end", "\n")
        self.chat_display.configure(state="disabled")

    def start_listening_thread(self):
        threading.Thread(target=self.listen_process).start()

    def listen_process(self):
        self.change_status("listening")
        self.user_input.delete(0, "end")
        self.user_input.configure(placeholder_text="Listening...")
        
        text = listen_audio()
        
        if text:
            self.user_input.insert(0, text)
            self.send_message()
        else:
            self.change_status("idle")
            self.user_input.configure(placeholder_text="Type your command here...")

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        message = self.user_input.get()
        if message.strip() == "":
            return

        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n👤 You: {message}\n")
        self.chat_display.configure(state="disabled")
        
        self.user_input.delete(0, "end")
        self.user_input.configure(placeholder_text="Type your command here...")

        threading.Thread(target=self.process_ai, args=(message,)).start()

    def process_ai(self, message):
        try:
            self.change_status("thinking")
            reply = ask_ai(message)
            
            self.change_status("speaking")
            
            # Typing aur Speaking
            self.typewriter_effect(reply)
            speak(reply)
            
            self.change_status("idle")
            
        except Exception as e:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"\n❌ SYSTEM ERROR: {e}\n")
            self.chat_display.configure(state="disabled")
            self.change_status("idle")

if __name__ == "__main__":
    app = ShakshiApp()
    app.mainloop()