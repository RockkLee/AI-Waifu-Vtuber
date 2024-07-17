import os
import torch
import requests
import urllib.parse
import time
from utils.katakana import *
from utils.elevenlab import elevenlab_tts
from playsound import playsound
from utils.tts_type import TtsType


# init
num_threads = os.cpu_count()
device = torch.device('cpu')
torch.set_num_threads(num_threads)
local_file = 'model.pt'
print(f"Using {num_threads} threads for silero_tts")
# load model.pt
cache_model = None
if os.path.isfile(local_file):
    print("Loading model.pt with cache...")
    cache_model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    cache_model.to(device)


# https://github.com/snakers4/silero-models#text-to-speech
def silero_tts(tts, language, model, speaker):
    if not os.path.isfile(local_file):
        print("Downloading model.pt...")
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/{language}/{model}.pt',
                                    local_file)  
        print("Loading model.pt...")
        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        global cache_model
        cache_model = model
    else:
        model = cache_model    
    model.to(device)

    example_text = "i'm fine thank you and you?"
    sample_rate = 48000

    audio_paths = model.save_wav(text=tts,
                                speaker=speaker,
                                sample_rate=sample_rate)


def voicevox_tts(tts):
    # You need to run VoicevoxEngine.exe first before running this script
    
    voicevox_url = 'http://localhost:50021'
    # Convert the text to katakana. Example: ORANGE -> オレンジ, so the voice will sound more natural
    katakana_text = katakana_converter(tts)
    # You can change the voice to your liking. You can find the list of voices on speaker.json
    # or check the website https://voicevox.hiroshiba.jp
    params_encoded = urllib.parse.urlencode({'text': katakana_text, 'speaker': 46})
    request = requests.post(f'{voicevox_url}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': 46, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{voicevox_url}/synthesis?{params_encoded}', json=request.json())

    with open("test.wav", "wb") as outfile:
        outfile.write(request.content)


def run_tts(type: TtsType, tts: str):
    if TtsType.SILERO == type:
        silero_tts(tts, "en", "v3_en", "en_50")
    elif TtsType.ELEVENTLAB == type:
        elevenlab_tts(tts)
    elif TtsType.VOICEVOX == type:
        pass


def play_tts(type: TtsType):
    if TtsType.SILERO == type:
        start_time = time.time()
        playsound('test.wav', block=True)
        print("---PlaySound: %s seconds ---" % (time.time() - start_time))
    elif TtsType.ELEVENTLAB == type:
        start_time = time.time()
        playsound('test.mp3', block=True)
        print("---PlaySound: %s seconds ---" % (time.time() - start_time))
    elif TtsType.VOICEVOX in type:
        pass