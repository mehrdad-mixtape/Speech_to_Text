from platform import platform
from typing import Generator
from wave import open
from pyaudio import PyAudio, paInt16
from speech_recognition import RequestError, UnknownValueError, Recognizer, AudioFile
import os, platform, sys

def _record_audio(name: str, time: int=3, chunk: int=1024, channels: int=2, sample_format: int=paInt16, sample_rate: int=30000):
    """Record Your Voice as *.wav file"""
    file_name: str = f'{name}.wav'
    try:
        p: PyAudio = PyAudio() # Create an interface to PortAudio
        if platform.system() == 'Windows': os.system('cls')
        elif platform.system() == 'Linux': os.system('clear')
        print('Recording ...')
        stream = p.open(
            format=sample_format,
            channels=channels,
            rate=sample_rate,
            frames_per_buffer=chunk,
            input=True
        )
        # Initialize array to store frames
        frames: list = [stream.read(chunk) for _ in range(0, int(sample_rate / chunk * time))] 
        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        # Save the recorded data as a WAV file
        with open(file_name, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
    except (Exception, KeyboardInterrupt): print('Finished recording.')
    finally: return file_name

def sTT(*args) -> Generator:
    file_name, time, *_ = args
    if isinstance(file_name, str) and isinstance(time, int): r: Recognizer = Recognizer()
    else: raise ValueError("args: 'file_name' should be string, 'time' should be 'int'")
    while True:
        try:
            speech: str = _record_audio(file_name, time)
            with AudioFile(speech) as source:
                # Listen for the data (load audio to memory)
                audio_data = r.record(source)
                # Recognize (convert from speech to text)
                text: str = r.recognize_google(audio_data)
                print(f"your request: {text}")

                if platform.system() == 'Windows': os.system(f"del {file_name}.wav")
                elif platform.system() == 'Linux': os.system(f"rm -rf {file_name}.wav")
                yield text
                input('Press Any Key To Continue, Or Press Ctrl+C')

        except KeyboardInterrupt: sys.exit('\nGoodBye.')
        except RequestError as RE: print(f"google cannot accept your request: {RE}")
        except UnknownValueError: print("Say something ..."); sys.exit("Say something ...")

def main() -> None:
    for text in sTT('output', 5): print(text)

if __name__ == "__main__":
    main()
    