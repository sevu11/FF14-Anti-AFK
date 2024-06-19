import tkinter as tk
from gui import Anti_AFK_GUI
import pyinstaller_versionfile

if __name__ == "__main__":
    root = tk.Tk()
    app = Anti_AFK_GUI(root)
    root.mainloop()