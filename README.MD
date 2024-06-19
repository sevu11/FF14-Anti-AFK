![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/sevu11/ffxiv-anti-afk/total)

# FFXIV Anti-AFK

## Changelog:
```
- 1.2 Updated UI and added logs.
- 1.1 Added input for key and store input to a json file for automatic loading on start. Some re-structure of the code logic.
- 1.0 First release
```

## Overview
This application prevents AFK (Away From Keyboard) status in the game "Final Fantasy XIV" by periodically sending keypresses.

![Demo](https://i.imgur.com/wZL9UIi.png)

## Usage

### Installation
1. **Download** the `Anti-AFK.exe` from the ![releases](https://github.com/sevu11/ffxiv-anti-afk/releases/latest) section or compile from source using pyinstaller.

### Running the Application
- Double-click `Anti-AFK.exe` to launch the application.
- Click on the "START" button to start, the application will send in a CTRL input every 10 minutes.
- Click on the "STOP" button to end the anti-AFK mechanism.
- Click on the "EXIT" button or close the window to quit the application.
- Update which key you wish to send. Default key is `CTRL`. 

### Build yourself
- Run `./build.ps1` to compile the app yourself.

## Known Issues
- Windows Defender or other antivirus software may flag the executable as potentially harmful due to its automation nature. Consider signing the executable or adding it to the whitelist.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request with your enhancements.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
