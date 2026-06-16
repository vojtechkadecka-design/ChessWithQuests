from model.game_logger import GameLogger
from model.herni_plocha import HerniPlocha
from model.revizor_tahu import RevizorTahu
from model.tah import Tah
from model.game_timer import GameTimer

class GameManager:
    def __init__(self):
        self.plocha(HerniPlocha)
        self.aktivni_hrac
        self.hraci
        self.aktualni_tah(Tah)
        self.casovac(GameTimer)
        self.game_logger(GameLogger)
        self.revizor_tahu(RevizorTahu)

    def proved_tah(self ):
        pass

    def zacni_tah(self):
        pass

    def mozne_tahy(self):
        pass

    def zrus_tah(self):
        pass

    def uloz_log(self):
        pass

    def get_stav(self):
        pass

    def najdi_uzivatele(self):
        pass