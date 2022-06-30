import numpy as np
import simpleaudio as sa
from threading import Thread


def play(file):
    def do(file):
        wave_obj = sa.WaveObject.from_wave_file("./sounds/" + file)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    doer = Thread(target=do, args=(file,))
    doer.start()


def nelson(prob=0.05):
    if np.random.random() < prob:
        play("haha.wav")

def point():
    play("point.wav")

def blue_card_point():
    play("super_point.wav")

if __name__ == "__main__":
    nelson()
