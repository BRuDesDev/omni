import pvporcupine
import pyaudio
import struct
import time
import pvporcupine


def main():

    """
    Creating our custom wake word FOR RASPI
    porcupine = pvporcupine.create(
         access_key="ZSLJLFCd+I7a0wOPRCRFrsSUNs9ZtEKvdNXtVTIXThBwN0IuelMGTg==",
         keyword_paths=['Yo-Omni_en_mac.ppn']
     )
    """

    # Creating our custom wake word FOR MAC
    porcupine = pvporcupine.create(
        access_key="rYuhw+G53e+ddvGxasAFgD+SMl00WMG7LWzLXrODAzSFw2bXJYD0hQ==",
        keyword_paths=['Yo-Omni_en_mac.ppn']
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Waiting for when I am needed...")
    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm_unpacked)
            if result >= 0:
                print("Wake word detected!")
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
