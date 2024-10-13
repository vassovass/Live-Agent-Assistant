
import logging
import tkinter as tk
from tkinter import scrolledtext

class UserInterface:
    def __init__(self, config, live_agent):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.live_agent = live_agent
        self.root = tk.Tk()
        self.root.title("AI Assistant Live Agent")
        self.setup_ui()

    def setup_ui(self):
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.chat_display.pack(padx=10, pady=10)

        self.input_field = tk.Entry(self.root, width=50)
        self.input_field.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

    def send_message(self):
        user_input = self.input_field.get()
        self.chat_display.insert(tk.END, f"You: {user_input}
")
        self.input_field.delete(0, tk.END)

        response = self.live_agent.process_input(user_input)
        self.chat_display.insert(tk.END, f"AI: {response}

")
        self.chat_display.see(tk.END)

    def run(self):
        self.root.mainloop()
