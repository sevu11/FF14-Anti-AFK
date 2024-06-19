import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import threading
import pyautogui
import pygetwindow as gw
import time
import json
import os
from datetime import datetime
from utils import resize_image, load_key, save_key

class Anti_AFK_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV: Anti AFK")
        self.root.configure(bg='#333333')

        self.bold_font = font.Font(family="Calibri", size=22, weight="bold")
        self.label_bold_font = font.Font(family="Calibri", size=30, weight="bold")

        self.logo = tk.PhotoImage(file='assets/logo.png')
        self.resized_logo = self.logo.subsample(2, 2)
        self.logo_label = tk.Label(root, image=self.resized_logo, bg='#333333')
        self.logo_label.pack(pady=20)

        button_width = 273
        button_height = 72
        
        self.start_img = resize_image('assets/start.png', button_width, button_height)
        self.stop_img = resize_image('assets/stop.png', button_width, button_height)
        self.quit_img = resize_image('assets/quit.png', button_width, button_height)

        self.start_button = tk.Button(root, image=self.start_img, command=self.start_sending, borderwidth=0, highlightthickness=0,
                                      highlightbackground='#333333', highlightcolor='#333333')
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, image=self.stop_img, command=self.stop_sending, state=tk.DISABLED, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.stop_button.pack(pady=10)

        self.quit_button = tk.Button(root, image=self.quit_img, command=self.quit_app, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.quit_button.pack(pady=10)

        separator = tk.Frame(root, height=2, bd=0, relief='sunken', bg='#333333')
        separator.pack(fill='x', pady=20)

        self.key_label = tk.Label(root, text="Select Key:", bg='#333333', fg='white', font=self.label_bold_font)
        self.key_label.pack(pady=(0,2), padx=(0,2))

        self.key_var = tk.StringVar()
        self.key_dropdown = ttk.Combobox(root, textvariable=self.key_var, 
                                         font=self.bold_font, 
                                         justify="center", 
                                         width=15, 
                                         background='white', 
                                         foreground='black')
        self.key_dropdown['values'] = ('Select Key', 'CTRL', 'ALT', 'W', 'A', 'S', 'D', 'SHIFT', '§', '<')
        self.key_dropdown.pack(pady=(20, 20))  

        combostyle = ttk.Style()
        combostyle.theme_use('xpnative')
        combostyle.configure('Custom.TCombobox', selectbackground='white', fieldbackground='white', foreground='black')
        combostyle.map('Custom.TCombobox', fieldbackground=[('readonly', 'white')])
                
        load_key(self.key_var)

        self.save_button = tk.Button(root, text="Save", 
                                     command=self.save_key_wrapper, 
                                     bg='#0b5fd9', 
                                     fg='white', 
                                     font=self.bold_font, 
                                     bd=0, 
                                     width=17,
                                     highlightthickness=0,
                                     activebackground='#2E59A3',
                                     activeforeground='white')
        
        self.save_button.pack(padx=20, pady=20)

        self.alert_label = tk.Label(root, text="", bg='#444444', fg='white', pady=20, font=self.bold_font)
        self.alert_label.pack(pady=(20, 20))
        self.alert_label.pack_forget()

        self.log_frame = tk.Frame(root)
        self.log_frame.pack(fill=tk.BOTH, expand=False)

        log_text_width = 5
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, bg='#444444', fg='white', font=('Consolas', 10), height=10, width=log_text_width, bd=0, padx=10, pady=5)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = self.log_scrollbar.set

        self.log_scrollbar.pack_forget()

        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        self.log_file = os.path.join(self.logs_dir, datetime.now().strftime("%Y-%m-%d") + ".log")
        self.is_running = False
        self.interval = 10 * 60
        self.target_window_title = "FINAL FANTASY XIV"
        
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
        while self.is_running:
            try:
                target_windows = gw.getWindowsWithTitle(self.target_window_title)
                for window in target_windows:
                    pyautogui.keyDown(self.key_var.get().lower())
                    time.sleep(0.1)
                    pyautogui.keyUp(self.key_var.get().lower())
                    self.log_message(f"Sent {self.key_var.get()}.")

                for _ in range(iterations):
                    if not self.is_running:
                        break
                    time.sleep(interval_check)
            except gw.PyGetWindowException as e:
                self.log_message(f"Error occurred: {e}")

    def start_sending(self):
        self.is_running = True
        
        load_key(self.key_var)
        
        if self.key_var.get() == 'Select Key':
            self.key_var.set('CTRL')
            save_key('ctrl')
        else:
            save_key(self.key_var.get().lower())
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.thread = threading.Thread(target=self.send_key)
        self.thread.start()
        
        self.log_message("Started.")

    def stop_sending(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.thread.is_alive():
            self.thread.join()
        self.log_message("Stopped.")

    def quit_app(self):
        self.is_running = False
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()
        self.root.quit()
        self.log_message("Application closed.")
