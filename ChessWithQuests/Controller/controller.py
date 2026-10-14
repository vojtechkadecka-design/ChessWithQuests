from model.game_manager import GameManager
from model.uzivatel import Uzivatel


class Controller:
    """Prostředník mezi Viewem (vstup/výstup) a GameManagerem (herní logika).

    View se nikdy nedotýká GameManageru přímo - jen dostává data z metod
    tohoto Controlleru a volá zpět jeho metody, když uživatel něco zadá."""

    def __init__(self, jmeno_bily="Bílý hráč", jmeno_cerny="Černý hráč"):
        uzivatel_bily = Uzivatel("hrac_bily", jmeno=jmeno_bily)
        uzivatel_cerny = Uzivatel("hrac_cerny", jmeno=jmeno_cerny)
        self.hra = GameManager(uzivatel_bily, uzivatel_cerny)

    def herni_deska(self):
        """Aktuální rozestavení figurek (8x8 seznam Figurka/None) pro View."""
        return self.hra.plocha.herni_deska

    def hrac_na_tahu(self):
        """Vrátí objekt Hrac, který je právě na tahu."""
        return self.hra.hraci[self.hra.aktivni_hrac]

    def zpracuj_tah(self, vychozi_pozice, cilova_pozice) -> bool:
        """Zkusí provést tah podle vstupu od Viewu. Vrátí True/False podle
        toho, zda byl tah platný a provedl se."""
        figurka = self.hra.plocha.vrat_obsah(vychozi_pozice)
        if figurka is None:
            return False

        tah = self.hra.zacni_tah()
        tah.vychozi_pozice = vychozi_pozice
        tah.cilova_pozice = cilova_pozice
        tah.figurka = figurka
        return self.hra.proved_tah(tah)

    def stav_hry(self) -> int:
        """0 = probíhá, 1 = šach, 2 = mat, 3 = pat (konstanty STAV_* v game_manager.py)."""
        return self.hra.get_stav()
