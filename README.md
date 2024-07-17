# Fork from ardha27/AI-Waifu-Vtuber
## Revised parts:
- Solved the dependencies issue in `pip install requirement.txt`
- oOptimized the silero_tts function

## Installation
- Please follow the instructions from original repo:
    - https://github.com/ardha27/AI-Waifu-Vtuber

## playsound.py
- This app uses a third-party audio lib, and due to the bug with files not being closed after playing, we need to revise the lib with the code below.
```python
    if block:
        sleep(float(durationInMS) / 1000.0)
        winCommand('close', alias) # Add this line to close the file after playing
```