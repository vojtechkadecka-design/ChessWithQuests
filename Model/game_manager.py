from model.herni_plocha import HerniPlocha
from model.revizor_tahu import RevizorTahu
from model.tah import Tah
from model.timer import Timer
from model.game_logger import GameLogger
from model.hrac import Hrac
from model.uzivatel import Uzivatel

STAV_PROBIHA = 0
STAV_SACH = 1
STAV_MAT = 2
STAV_PAT = 3


class GameManager:
    def __init__(self, uzivatel_bily: Uzivatel, uzivatel_cerny: Uzivatel):
        self.plocha = HerniPlocha()
        self.hraci = [Hrac(1, uzivatel_bily), Hrac(-1, uzivatel_cerny)]
        self.aktivni_hrac = 0        # index do self.hraci; 0 = bílý na tahu
        self.aktualni_tah = None
        self.casovac = Timer()
        self.game_logger = GameLogger()
        self.revizor_tahu = RevizorTahu(self.plocha)

    def zacni_tah(self) -> Tah:
        """Založí nový (zatím prázdný) tah pro hráče, který je právě na tahu.
        Volající (viz main.py) poté na vráceném objektu nastaví
        vychozi_pozice, cilova_pozice a figurka - teprve pak ho lze předat
        do proved_tah()."""
        self.aktualni_tah = Tah(None, None, None)
        return self.aktualni_tah

    def mozne_tahy(self):
        """Vrátí seznam všech legálních tahů (Tah) pro hráče, který je právě
        na tahu. Legální = geometricky platný a zároveň nenechává vlastního
        krále v šachu."""
        barva = self.hraci[self.aktivni_hrac].barva
        vysledek = []
        for radek in range(8):
            for sloupec in range(8):
                figurka = self.plocha.herni_deska[radek][sloupec]
                if figurka is None or figurka.barva != barva:
                    continue
                for radek_do in range(8):
                    for sloupec_do in range(8):
                        tah = Tah((radek, sloupec), (radek_do, sloupec_do), figurka)
                        if not tah.over_platnost(self.plocha):
                            continue
                        nova_mrizka = self.revizor_tahu.simulate_move(tah)
                        if not self.revizor_tahu.check_sach(barva, nova_mrizka):
                            vysledek.append(tah)
        return vysledek

    def proved_tah(self, tah: Tah) -> bool:
        """V diagramu není popsáno, jak se vybraný tah skutečně provede a
        předá na tahu dalšímu hráči - tuhle metodu jsem proto musel přidat.
        Provede tah, pokud je mezi možnými tahy aktivního hráče, zaloguje ho
        a předá tah druhému hráči."""
        if tah.figurka is None or tah.vychozi_pozice is None or tah.cilova_pozice is None:
            return False

        legalni = any(t.vychozi_pozice == tah.vychozi_pozice
                      and t.cilova_pozice == tah.cilova_pozice
                      for t in self.mozne_tahy())
        if not legalni:
            return False

        tah.proved_tah(self.plocha)
        self.revizor_tahu.tah = tah
        self.uloz_log()
        self.aktivni_hrac = 1 - self.aktivni_hrac
        return True

    def zrus_tah(self) -> None:
        self.aktualni_tah = None

    def uloz_log(self) -> None:
        if self.aktualni_tah is not None:
            self.game_logger.uloz_tah(self.aktualni_tah)

    def get_stav(self) -> int:
        """Vrátí stav hry vzhledem k hráči, který je právě na tahu."""
        if self.revizor_tahu.check_mat:
            return STAV_MAT
        if self.revizor_tahu.check_pat:
            return STAV_PAT
        barva = self.hraci[self.aktivni_hrac].barva
        if self.revizor_tahu.check_sach(barva):
            return STAV_SACH
        return STAV_PROBIHA

    def najdi_uzivatele(self, id: int) -> Uzivatel:
        """Zjednodušený vyhledávač - v tomto projektu není databáze
        uživatelů, skutečné hledání podle id by řešila samostatná vrstva/DB."""
        for hrac in self.hraci:
            if getattr(hrac.uzivatel, "id", None) == id:
                return hrac.uzivatel
        return None
