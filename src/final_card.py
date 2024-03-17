from .card import Card, AxBorder


class Final_Card:
    def __init__(self, player):
        self.player = player
        self.active = False

    def active(self, idx):
        self.idx = idx

    def submit(self):
        pass

    def end(self):
        pass

    def draw(self):
        pass