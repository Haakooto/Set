import numpy as np
import simpleaudio as sa
from threading import Thread


def play(file):
    def do(file):
<<<<<<< HEAD
        wave_obj = sa.WaveObject.from_wave_file("sounds/" + file)
=======
        wave_obj = sa.WaveObject.from_wave_file("./sounds/" + file)
>>>>>>> d09ee44a437790c55b4d15eb0da6a9d14e614efb
        play_obj = wave_obj.play()
        play_obj.wait_done()

    doer = Thread(target=do, args=(file,))
    doer.start()


def nelson():
    if np.random.random() < 0.05:   
        play("haha.wav")


if __name__ == "__main__":
    nelson()
