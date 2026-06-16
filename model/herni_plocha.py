from model.figurka import Figurka
from model.tah import Tah


class HerniPlocha:
    def __init__(self):
        self.rozmery = [(8,8)]
        self.herni_deska = [(())]
        self.vyhozené_figurky_1 = []
        self.vyhozene_figurky_1 = []
        self.tah(Tah)
        self.figurka(Figurka)

    def posun_figurky(self):
        pass

    def nahrad_figurku(self):
        pass


