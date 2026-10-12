from model.game_manager import GameManager

class Controller:
    def __init__(self, uzivatel_bily, uzivatel_cerny):
        self.hra = GameManager(uzivatel_bily, uzivatel_cerny)

    def zpracuj_tah(self, vychozi_pozice, cilova_pozice) -> bool:
        tah = self.hra.zacni_tah()
        tah.vychozi_pozice = vychozi_pozice
        tah.cilova_pozice = cilova_pozice
        tah.figurka = self.hra.plocha.vrat_obsah(vychozi_pozice)
        if tah.figurka is None:
            return False
        return self.hra.proved_tah(tah)

    def stav_hry(self) -> int:
        return self.hra.get_stav()