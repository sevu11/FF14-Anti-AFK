import customtkinter as ctk
import tkinter as tk
import threading
import pyautogui
import time
import json
import os
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from utils import load_key, save_key
from Xlib import X, display
from ewmh import EWMH
from pynput import keyboard
import subprocess 

class Anti_AFK_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV: Anti AFK")
        self.root.configure(bg='#333333')

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.bold_font = ctk.CTkFont(family="Calibri", size=45, weight="bold")
        self.label_bold_font = ctk.CTkFont(family="Calibri", size=45, weight="bold")

        self.logo_image = Image.open('assets/logo.png')
        self.resized_logo = self.logo_image.resize((300, 300), Image.LANCZOS)

        self.logo_ctk_image = ctk.CTkImage(
            light_image=self.resized_logo,
            dark_image=self.resized_logo,
            size=(600, 300)
        )
        
        self.logo_label = ctk.CTkLabel(root, image=self.logo_ctk_image, text="", fg_color='#333333')
        self.logo_label.pack(pady=20)

        self.start_button = ctk.CTkButton(root, text="Start", command=self.start_sending, font=self.bold_font, 
                                          fg_color='#3B71CA', text_color='white', hover_color='#5078DC')
        self.start_button.pack(pady=10)
        
        self.stop_button = ctk.CTkButton(root, text="Stop", command=self.stop_sending, font=self.bold_font, 
                                         fg_color='#9FA6B2', text_color='white', hover_color='#BEC8D7', state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(root, text="Quit", command=self.quit_app, font=self.bold_font, 
                                         fg_color='#DC4C64', text_color='white', hover_color='#F57887')
        self.quit_button.pack(pady=10)
        
        separator = ctk.CTkFrame(root, height=2, corner_radius=0, fg_color="#333333")
        separator.pack(fill='x', pady=20)

        self.key_label = ctk.CTkLabel(root, text="Select Key:", font=self.label_bold_font)
        self.key_label.pack(pady=(0,2), padx=(0,2))

        self.key_var = tk.StringVar()
        self.key_dropdown = ctk.CTkComboBox(root, variable=self.key_var, font=ctk.CTkFont(family="Calibri", size=30, weight="bold"), width=170, state='readonly', justify="center")
        self.key_dropdown.configure(values=('Select Key', 'CTRL', 'ALT', 'W', 'A', 'S', 'D', 'SHIFT', '§', '<'))
        self.key_dropdown.pack(pady=(20, 20))

        load_key(self.key_var)

        self.save_button = ctk.CTkButton(root, text="Save", command=self.save_key_wrapper, font=self.bold_font, 
                                         fg_color='#5cb85c', text_color='white', hover_color='#4cae4c')
        self.save_button.pack(padx=20, pady=20)
        
        self.alert_label = ctk.CTkLabel(root, text="", font=self.bold_font)
        self.alert_label.pack(pady=(20, 20))
        self.alert_label.pack_forget()

        self.log_frame = ctk.CTkFrame(root)
        self.log_frame.pack(fill=tk.BOTH, expand=False)

        log_text_font = tk.font.Font(family="Consolas", size=12)
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, height=10, width=5, padx=10, pady=5, bg='#202020', fg='white', bd=0, font=log_text_font)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_scrollbar = ctk.CTkScrollbar(self.log_frame, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = self.log_scrollbar.set
        self.log_scrollbar.pack_forget()

        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        self.log_file = os.path.join(self.logs_dir, datetime.now().strftime("%Y-%m-%d") + ".log")
        self.is_running = False
        self.interval = 10 * 60
        self.target_window_title = "FINAL FANTASY XIV"

        self.keybind = keyboard.Key.f12  # Default value
        self.load_config()  # Load config values

        self.listener_thread = threading.Thread(target=self.key_listener)
        self.listener_thread.daemon = True
        self.listener_thread.start()
                
    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
                self.key_var.set(config.get("key", "CTRL"))
                self.keybind = getattr(keyboard.Key, config.get("start_stop_key", "F12").lower())
        except Exception as e:
            self.log_message(f"Error loading config: {e}")
        
    def show_alert(self, message):
        self.alert_label.config(text=message)
        self.alert_label.pack(pady=25, padx=25)
        self.root.after(5000, self.hide_alert)

    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        full_message = f"[{timestamp}] - {message}"
        self.log_text.insert(tk.END, full_message + '\n')
        self.log_text.see(tk.END)
        with open(self.log_file, "a") as log:
            log.write(full_message + '\n')

    def save_key_wrapper(self):
        selected_key = self.key_var.get()
        save_key(selected_key.lower())
        self.log_message(f"Key {selected_key.upper()} saved.")

    def hide_alert(self):
        self.alert_label.pack_forget()

    def send_key(self):
        interval_check = 1
        iterations = self.interval // interval_check
        ewmh = EWMH()
        
        while self.is_running:
            try:
                root = display.Display().screen().root
                window_ids = root.get_full_property(
                    ewmh.display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType
                ).value
                
                target_window_found = False
                
                for window_id in window_ids:
                    window = ewmh.display.create_resource_object('window', window_id)
                    window_title = window.get_full_property(
                        ewmh.display.intern_atom('_NET_WM_NAME'), 0
                    ).value
                    if window_title.decode('utf-8') == self.target_window_title:
                        target_window_found = True
                        # Activate the window using xdotool
                        subprocess.run(["xdotool", "windowactivate", str(window_id)])
                        break

                if target_window_found:
                    pyautogui.keyDown(self.key_var.get().lower())
                    time.sleep(0.1)
                    pyautogui.keyUp(self.key_var.get().lower())
                    self.log_message(f"Sent {self.key_var.get()} key.")
                    
                    end_time = datetime.now() + timedelta(seconds=self.interval)
                    self.log_message(f"On cooldown until [{end_time.strftime('%H:%M:%S')}]...")
                            
                    for _ in range(iterations):
                        if not self.is_running:
                            break
                        time.sleep(interval_check)
                else:
                    self.log_message("Target window not found.")
                    time.sleep(interval_check)
            except Exception as e:
                self.log_message(f"Error occurred: {e}")

    def start_sending(self):
        self.is_running = True
        
        load_key(self.key_var)
        
        if self.key_var.get() == 'Select Key':
            self.key_var.set('CTRL')
            save_key('ctrl')
        else:
            save_key(self.key_var.get().lower())
        
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        
        self.thread = threading.Thread(target=self.send_key)
        self.thread.start()
        
        self.log_message("Started")

    def stop_sending(self):
        self.is_running = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        if self.thread.is_alive():
            self.thread.join()
        self.log_message("Stopped")

    def quit_app(self):
        self.is_running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
        self.root.destroy()
    
    def on_key_press(self, key):
        try:
            if key == self.keybind:
                if self.is_running:
                    self.stop_sending()
                else:
                    self.start_sending()
        except Exception as e:
            self.log_message(f"Error in key listener: {e}")

    def key_listener(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

if __name__ == "__main__":
    root = ctk.CTk()
    app = Anti_AFK_GUI(root)
    root.mainloop()
