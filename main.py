import tkinter as tk
from PIL import Image, ImageTk
import threading
import pyautogui
import pygetwindow as gw
import time
import sys

class Anti_AFK_APP:
    def __init__(self, root):
        self.root = root
        self.root.title("FFXIV: Anti AFK")
        self.root.configure(bg='#333333')
        
        self.logo = tk.PhotoImage(file='logo.png')
        self.resized_logo = self.logo.subsample(3, 3)
        self.logo_label = tk.Label(root, image=self.resized_logo, bg='#333333')
        self.logo_label.pack(pady=20)
        
        button_width = 243
        button_height = 62
        
        self.start_img = self.resize_image('start.png', button_width, button_height)
        self.stop_img = self.resize_image('stop.png', button_width, button_height)
        self.quit_img = self.resize_image('quit.png', button_width, button_height)
        
        self.start_button = tk.Button(root, image=self.start_img, command=self.start_sending, borderwidth=0, highlightthickness=0,
                                      highlightbackground='#333333', highlightcolor='#333333')
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, image=self.stop_img, command=self.stop_sending, state=tk.DISABLED, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.stop_button.pack(pady=10)
        
        self.quit_button = tk.Button(root, image=self.quit_img, command=self.quit_app, borderwidth=0, highlightthickness=0,
                                     highlightbackground='#333333', highlightcolor='#333333')
        self.quit_button.pack(pady=20)
        
        self.is_running = False
        self.interval = 10 * 60
        self.target_window_title = "FINAL FANTASY XIV"

    def resize_image(self, filename, width, height):
        img = Image.open(filename)
        img = img.resize((width, height), resample=Image.BILINEAR)
        return ImageTk.PhotoImage(img)
        
    def send_key(self):
        try:
            target_windows = gw.getWindowsWithTitle(self.target_window_title)
            
            for window in target_windows:
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.keyUp('ctrl')
                
        except gw.PyGetWindowException as e:
            print(f"Error occurred: {e}")
        
        if self.is_running:
            self.root.after(self.interval * 1000, self.send_key)
    
    def start_sending(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.send_key()
        
    def stop_sending(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def quit_app(self):
        self.is_running = False
        self.root.quit()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = Anti_AFK_APP(root)
    root.mainloop()
