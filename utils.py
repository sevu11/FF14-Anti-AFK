from PIL import Image, ImageTk
import json
import os

def resize_image(filename, width, height):
    img = Image.open(filename)
    img = img.resize((width, height), resample=Image.BILINEAR)
    return ImageTk.PhotoImage(img)

def load_key(key_var):
    default_key = 'Select Key'
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as file:
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
    else:
        print("Config file 'config.json' not found.")
    
    key_var.set(default_key)

def save_key(selected_key):
    selected_key_lower = selected_key.lower()
    try:
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump({'key': selected_key_lower}, file)
    except Exception as e:
        print(f"Error saving key to config file: {e}")
