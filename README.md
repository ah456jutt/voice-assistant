# Voice Assistant

A versatile voice assistant that can handle both voice and text commands, execute system operations, and provide interactive responses.

## Features

- **Dual Mode Operation**
  - Voice command mode with speech recognition
  - Text command mode for typed inputs

- **System Commands**
  - Execute basic Windows commands (ipconfig, hostname, dir, etc.)
  - Get system information
  - Check date and time
  - Monitor system resources

- **Interactive Responses**
  - Natural language processing
  - Friendly chat responses
  - Command confirmation
  - Error handling

## Requirements

- Python 3.8 or higher
- Windows OS
- Microphone (for voice mode)
- Speakers/Headphones

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ah456jutt/voice-assistant.git
cd voice-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the assistant:
```bash
python src/main.py
```

### Available Commands

1. **System Information**
   - `hostname` - Display computer name
   - `whoami` - Show current user
   - `ipconfig` - Show network configuration
   - `systeminfo` - Display system details

2. **Time and Date**
   - `time` - Show current time
   - `date` - Show current date

3. **Chat Commands**
   - `hello`
   - `how are you`
   - `thank you`
   - `i like you`
   - `i love you`

4. **Help**
   - `help` or `commands` - Show available commands

### Voice Mode Tips
- Speak clearly and at a normal pace
- Wait for the "Listening..." prompt
- Keep background noise to a minimum

### Text Mode Tips
- Commands are case-insensitive
- Type 'exit' or 'goodbye' to quit

## Project Structure

```
voice-assistant/
├── src/
│   ├── main.py
│   └── assistant/
│       ├── __init__.py
│       ├── task_manager.py
│       └── system_control.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Ahmad Hassan** - [ah456jutt](https://github.com/ah456jutt)

## Acknowledgments

- Speech Recognition library
- pyttsx3 for text-to-speech
- sounddevice for audio processing
- All contributors and testers

## Contact

- GitHub: [@ah456jutt](https://github.com/ah456jutt)