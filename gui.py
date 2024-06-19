import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import pyautogui
import pygetwindow as gw
import time
import json
import os
from utils import resize_image

class Anti_AFK_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV: Anti AFK")
        self.root.configure(bg='#333333')

        self.alert_label = tk.Label(root, text="", bg='#444444', fg='white', pady=20, font=('Arial', 20))
        self.alert_label.pack(pady=(20, 20))
        self.alert_label.pack_forget()

        self.logo = tk.PhotoImage(file='logo.png')
        self.resized_logo = self.logo.subsample(3, 3)
        self.logo_label = tk.Label(root, image=self.resized_logo, bg='#333333')
        self.logo_label.pack(pady=20)

        button_width = 273
        button_height = 72
        self.start_img = resize_image('start.png', button_width, button_height)
        self.stop_img = resize_image('stop.png', button_width, button_height)
        self.quit_img = resize_image('quit.png', button_width, button_height)

        self.start_button = tk.Button(root, image=self.start_img, command=self.start_sending, borderwidth=0, highlightthickness=0,
                                      highlightbackground='#333333', highlightcolor='#333333')
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, image=self.stop_img, command=self.stop_sending, state=tk.DISABLED, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.stop_button.pack(pady=10)

        self.quit_button = tk.Button(root, image=self.quit_img, command=self.quit_app, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.quit_button.pack(pady=20)

        self.key_label = tk.Label(root, text="Set Key:", bg='#333333', fg='white', font=('Arial', 20))
        self.key_label.pack(pady=(10, 10))

        self.key_var = tk.StringVar()
        self.key_dropdown = ttk.Combobox(root, textvariable=self.key_var, font=('Arial', 20))
        self.key_dropdown['values'] = ('CTRL', 'ALT', 'W', 'A', 'S', 'D', 'SHIFT')
        self.key_dropdown.pack(pady=(20, 20))  

        self.load_key()

        self.save_button = tk.Button(root, text="Save", command=self.save_key, bg='#444444', fg='white', font=('Arial', 20))
        self.save_button.pack(pady=20)

        self.is_running = False
        self.interval = 10 * 60
        self.target_window_title = "FINAL FANTASY XIV"

    def load_key(self):
        default_key = 'CTRL'
        if os.path.exists('config.json'):
            with open('config.json', 'r') as file:
                config = json.load(file)
                default_key = config.get('key', 'ctrl').lower()
        self.key_var.set(default_key)

    def save_key(self):
        selected_key = self.key_var.get()
        selected_key_lower = selected_key.lower()
        self.show_alert(f"Key {selected_key.upper()} saved successfully!")

        with open('config.json', 'w') as file:
            json.dump({'key': selected_key_lower}, file)

    def show_alert(self, message):
        self.alert_label.config(text=message)
        self.alert_label.pack(pady=25, padx=25)
        self.root.after(5000, self.hide_alert)

    def hide_alert(self):
        self.alert_label.pack_forget()

    def send_key(self):
        while self.is_running:
            try:
                target_windows = gw.getWindowsWithTitle(self.target_window_title)

                for window in target_windows:
                    pyautogui.keyDown(self.key_var.get())
                    time.sleep(0.1)
                    pyautogui.keyUp(self.key_var.get())

            except gw.PyGetWindowException as e:
                print(f"Error occurred: {e}")

            time.sleep(self.interval)

    def start_sending(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.send_key)
        self.thread.start()

    def stop_sending(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.thread.is_alive():
            self.thread.join()

    def quit_app(self):
        self.is_running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
        self.root.quit()
