import customtkinter as ctk
import tkinter as tk
import keyboard
import ctypes
import threading
import time

class FastAutoClicker:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.click_thread = None
        self.hotkey = 'ctrl+z'  # default
        self.ui = None

    def fast_click(self):
        user32 = ctypes.windll.user32
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004
        while not self.stop_event.is_set():
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def toggle(self):
        if self.running:
            self.running = False
            self.stop_event.set()
            if self.click_thread and self.click_thread.is_alive():
                self.click_thread.join()
            self.stop_event.clear()
            self.ui.update_status("Stopped")
        else:
            self.running = True
            self.click_thread = threading.Thread(target=self.fast_click)
            self.click_thread.start()
            self.ui.update_status("Running")

    def set_hotkey(self, hotkey):
        keyboard.unhook_all_hotkeys()  # unhook all hotkeys
        self.hotkey = hotkey
        keyboard.add_hotkey(self.hotkey, self.toggle)
        self.ui.update_status(f"Hotkey updated to: {hotkey}")

    def start(self):
        keyboard.add_hotkey(self.hotkey, self.toggle)
        self.ui = AutoClickerUI(self)
        self.ui.run()

class AutoClickerUI:
    def __init__(self, clicker):
        self.clicker = clicker
        self.window = ctk.CTk()
        self.window.title("Auto-Clicker")

        # configure the window appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create and place widgets
        self.hotkey_label = ctk.CTkLabel(self.window, text=f"Current Hotkey: {self.clicker.hotkey}", font=("Arial", 16))
        self.hotkey_label.pack(pady=10)

        self.hotkey_button = ctk.CTkButton(self.window, text="Click to Set Hotkey", command=self.start_hotkey_input, font=("Arial", 14))
        self.hotkey_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.window, text="Status: Stopped", font=("Arial", 14))
        self.status_label.pack(pady=10)

    def update_status(self, status):
        self.status_label.configure(text=f"Status: {status}")

    def start_hotkey_input(self):
        self.update_status("Updating hotkey...")
        self.window.bind("<Key>", self.set_hotkey_from_keypress)
        self.window.bind("<FocusOut>", self.reset_key_bind)

    def set_hotkey_from_keypress(self, event):
        key = event.keysym
        modifiers = []
        if event.state & 0x0004:  # control
            modifiers.append("ctrl")
        if event.state & 0x0001:  # shift
            modifiers.append("shift")
        if event.state & 0x0008:  # alt
            modifiers.append("alt")

        hotkey = "+".join(modifiers + [key.lower()])
        self.clicker.set_hotkey(hotkey)
        self.reset_key_bind(None)

    def reset_key_bind(self, event):
        self.window.unbind("<Key>")

    def run(self):
        self.window.mainloop()

# start up
clicker = FastAutoClicker()
clicker.start()
