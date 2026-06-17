from model.figurka import Figurka
from model.tah import Tah


class HerniPlocha:
    def __init__(self):
        self.rozmery = [(8,8)]
        self.herni_deska = [[Figurka]]
        self.vyhozene_figurky_1 = [Figurka]
        self.vyhozene_figurky_2 = [Figurka]
        self.tah(Tah)
        self.figurka(Figurka)

    def posun_figurky(self):
        pass

    def nahrad_figurku(self):
        pass

    #def vrat_obsah(self):  podle mě zbytečné
       #pass


