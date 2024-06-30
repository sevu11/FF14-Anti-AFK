from PIL import Image, ImageTk
import json
import os
from pynput import keyboard 

CONFIG_FILE = 'config.json'

def resize_image(filename, width, height):
    img = Image.open(filename)
    img = img.resize((width, height), resample=Image.BILINEAR)
    return ImageTk.PhotoImage(img)

def load_key(key_var):
    default_key = 'Select Key'
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
                key_from_config = config.get('key', 'Select Key').upper()
                if key_from_config == 'SELECT KEY':
                    config['key'] = 'ctrl'
                    key_from_config = 'CTRL'
                else:
                    key_from_config = key_from_config.upper()
                default_key = key_from_config
        except Exception as e:
            print(f"Error loading key from config file: {e}")
    
    key_var.set(default_key)

def save_key(selected_key):
    selected_key_lower = selected_key.lower()
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
        config['key'] = selected_key_lower
        # Ensure to also save the start_stop_key if it exists, or set it to 'F12'
        if 'start_stop_key' in config:
            config['start_stop_key'] = config['start_stop_key']
        else:
            config['start_stop_key'] = 'f12'
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file)
    except Exception as e:
        print(f"Error saving key to config file: {e}")

def load_start_stop_key():
    default_start_stop_key = 'f12'
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
                start_stop_key = config.get('start_stop_key', default_start_stop_key).lower()
                return getattr(keyboard.Key, start_stop_key)
        except Exception as e:
            print(f"Error loading start/stop key from config file: {e}")
    return getattr(keyboard.Key, default_start_stop_key)

def save_start_stop_key(start_stop_key):
    start_stop_key_lower = start_stop_key.lower()
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                config = json.load(file)
        config['start_stop_key'] = start_stop_key_lower
        # Ensure to also save the key if it exists, or set it to 'CTRL'
        if 'key' in config:
            config['key'] = config['key']
        else:
            config['key'] = 'ctrl'
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file)
    except Exception as e:
        print(f"Error saving start/stop key to config file: {e}")
