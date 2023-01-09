# stream audio file and default input device to default output device


"""imports"""


from defs import device_to_device_stream, audio_file_stream

import pyaudio
import multiprocessing as mp


"""run it all"""


if __name__ == '__main__':
    # multiprocessing freeze support enabling
    mp.freeze_support()

    # take indexes of default audio devices
    pa = pyaudio.PyAudio()
    input_index = pa.get_default_input_device_info()["index"]
    output_index = pa.get_default_output_device_info()["index"]

    # run stream of test audio file to default output device
    process = mp.Process(target=audio_file_stream, args=(["test_1.mp3"], output_index, -20))
    process.start()

    # run stream of default input device to default output device
    process = mp.Process(target=device_to_device_stream, args=(input_index, output_index, 0.05))
    process.start()






