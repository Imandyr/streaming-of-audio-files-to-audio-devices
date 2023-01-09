# functions for playing audio file and input audio device sound to output audio device


"""imports"""


import pyaudio
import pydub

import os
import numpy as np


"""functions"""


# play audio file to some output device
def audio_file_stream(file_path, device_index:int, sound_volume:float, frames_per_buffer:int=1024):
    """
    function for playing one audio file to some output device
    :param file_path: string or list of strings with paths to .mp3 audio files
    :param device_index: index of target output device
    :param sound_volume: value in dBs for changing volume of streaming sound
    :param frames_per_buffer: stream frames per buffer
    :return: playing audio file at target output device
    """

    # iterate path list
    for path in np.asarray(file_path).reshape([-1]):

        # initialize PyAudio() object
        pa = pyaudio.PyAudio()

        # load .mp3 file, convert to .wav file
        if not os.path.exists(f"{path[:-4]}.wav"):
            sound = pydub.AudioSegment.from_mp3(path)
            sound.export(f"{path[:-4]}.wav", format="wav")

        # load audio in .wav file
        wav_file = pydub.AudioSegment.from_wav(f"{path[:-4]}.wav")
        # change volume of sound in dBs
        wav_file = wav_file + sound_volume

        # create output audio stream to device
        stream = pa.open(rate=wav_file.frame_rate, channels=wav_file.channels,
                         format=pa.get_format_from_width(wav_file.sample_width),
                         frames_per_buffer=frames_per_buffer,
                         output=True, output_device_index=device_index)

        # write audio frames to stream
        stream.write(wav_file.raw_data)

        # close stream and pyaudio
        stream.stop_stream()
        stream.close()
        pa.terminate()


# stream sound from input device to output device
def device_to_device_stream(input_device_index:int, output_device_index:int, input_read_rate:float,
                        rate:int=44100, channels:int=2, frames_per_buffer:int=1024, format=pyaudio.paInt16):
    """
    stream sound from input device to output device
    :param input_device_index: index of input device
    :param output_device_index: index of output device
    :param input_read_rate: read every int(input_read_rate*rate) of input device waves and write to output
    :param rate: stream audio rate
    :param channels: stream audio channels
    :param frames_per_buffer: stream audio frames per buffer
    :param format: stream audio format
    :return: stream sound from one input device to one output device
    """

    # initialize PyAudio() object
    pa = pyaudio.PyAudio()

    # create audio stream from input to output
    stream = pa.open(rate=rate,
                     channels=channels, format=format, frames_per_buffer=frames_per_buffer,
                     output=True, input=True, input_device_index=input_device_index,
                     output_device_index=output_device_index)

    # read every int(input_read_rate*rate) of input device waves and write to output device
    while True:
        # read batch of audio input and write to output
        stream.write(frames=stream.read(num_frames=int(input_read_rate * rate)))





