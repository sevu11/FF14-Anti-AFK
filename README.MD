# FFXIV Anti-AFK

## Overview
This application prevents AFK (Away From Keyboard) status in the game "Final Fantasy XIV" by periodically sending keypresses.

## Usage

### Installation
1. **Download** the `Anti-AFK.exe` from the releases section or compile from source using pyinstaller.

### Running the Application
- Double-click `Anti-AFK.exe` to launch the application.
- Click on the "START" button to start, the application will send in a CTRL input every 10 minutes.
- Click on the "STOP" button to end the anti-AFK mechanism.
- Click on the "EXIT" button or close the window to quit the application.

### Customization
- Adjust the interval (`self.interval` in `main.py`) to change the frequency of key presses.
- Replace `logo.png`, `start.png`, `stop.png`, and `quit.png` with your own images if desired.

## Known Issues
- Windows Defender or other antivirus software may flag the executable as potentially harmful due to its automation nature. Consider signing the executable or adding it to the whitelist.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request with your enhancements.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.