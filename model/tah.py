from model.figurka import Figurka


class Tah:
    def __init__(self):
        self.vychozi_pozice = [()]
        self.cilova_pozice = (())
        self.figurka(Figurka)
        self.typ_tahu = ""

    def over_platnost(self):
        return bool

    def proved_tah(self):
        pass