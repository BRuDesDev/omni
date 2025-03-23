import pyaudio
import struct
import time
import pvporcupine
import json
from datetime import datetime
import boto3

# Adjust these constants for your Pi-specific .ppn filename and your valid access key
WAKE_WORD_PATH = "Hey-Omni-en-raspi.ppn"
PLATFORM_ACCESS_KEY = "ZSLJLFCd+I7a0wOPRCRFrsSUNs9ZtEKvdNXtVTIXThBwN0IuelMGTg=="


def log_conversation(user_text, assistant_text):
    """
    :param user_text: The transcribed text from user
    :param assistant_text: The response to the user_text from GPT model
    :return: None
    """
    with open("conversations.json", "r") as f:
        data = json.load(f)

    # If you have some session management in place
    entry = {
        "timestamp": str(datetime.now()),
        "user": user_text,
        "assistant": assistant_text
    }
    data.append(entry)

    with open("conversations.json", "w") as f:
        json.dump(data, f, indent=2)


def main():
    # Create Porcupine with Raspberry Pi–specific settings
    porcupine = pvporcupine.create(
        access_key=PLATFORM_ACCESS_KEY,
        keyword_paths=[WAKE_WORD_PATH]
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word on Raspberry Pi...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm_unpacked)
            if result >= 0:
                print("Yes sir...? (Wake word detected)")
                time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


if __name__ == "__main__":
    main()
