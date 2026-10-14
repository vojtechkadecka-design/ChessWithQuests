from model.tah import Tah
from model.figurka import Kral
from model.herni_plocha import HerniPlocha


class RevizorTahu:
    def __init__(self, herni_plocha):
        self.herni_plocha = herni_plocha
        self.tah = None   # poslední odehraný tah - podle něj se pozná, čí
                          # král se má kontrolovat v check_mat/check_pat

    @staticmethod
    def _plocha_z_mrizky(mrizka):
        """Zabalí syrovou mřížku (seznam seznamů) do HerniPlochy (bez
        rozestavění výchozí pozice), aby šlo znovu použít Tah.over_platnost()
        / proved_tah() i pro simulované a pomocné mřížky - bez zvláštního
        modulu navíc jen s pravidly."""
        plocha = HerniPlocha.__new__(HerniPlocha)
        plocha.rozmery = (8, 8)
        plocha.herni_deska = mrizka
        plocha.vyhozene_figurky_b = []
        plocha.vyhozene_figurky_c = []
        return plocha

    def simulate_move(self, tah) -> list:
        """Vrátí novou herní mřížku (seznam) s již provedeným tahem, beze
        změny skutečné hry."""
        mrizka = [radek[:] for radek in self.herni_plocha.herni_deska]
        docasna_plocha = self._plocha_z_mrizky(mrizka)
        tah_na_kopii = Tah(tah.vychozi_pozice, tah.cilova_pozice, tah.figurka, tah.typ_tahu)
        tah_na_kopii.proved_tah(docasna_plocha)
        return docasna_plocha.herni_deska

    def _najdi_krale(self, herni_deska, barva):
        for radek in range(8):
            for sloupec in range(8):
                f = herni_deska[radek][sloupec]
                if isinstance(f, Kral) and f.barva == barva:
                    return (radek, sloupec)
        return None

    def check_sach(self, barva, herni_deska=None) -> bool:
        """Je král dané barvy v šachu na dané (nebo aktuální) mřížce?"""
        if herni_deska is None:
            herni_deska = self.herni_plocha.herni_deska

        pozice_krale = self._najdi_krale(herni_deska, barva)
        if pozice_krale is None:
            return False

        docasna_plocha = self._plocha_z_mrizky(herni_deska)
        for radek in range(8):
            for sloupec in range(8):
                figurka = herni_deska[radek][sloupec]
                if figurka is not None and figurka.barva != barva:
                    # Dočasný Tah jen pro ověření, že figurka "dosáhne" na pole
                    # krále - využívá stejnou logiku jako skutečný tah.
                    docasny_tah = Tah((radek, sloupec), pozice_krale, figurka)
                    if docasny_tah.over_platnost(docasna_plocha):
                        return True
        return False

    def _existuje_tah_bez_sachu(self, barva) -> bool:
        """Existuje alespoň jeden legální tah hráče dané barvy, který ho
        nenechá v šachu?"""
        herni_deska = self.herni_plocha.herni_deska
        docasna_plocha = self._plocha_z_mrizky(herni_deska)
        for radek in range(8):
            for sloupec in range(8):
                figurka = herni_deska[radek][sloupec]
                if figurka is None or figurka.barva != barva:
                    continue
                for radek_do in range(8):
                    for sloupec_do in range(8):
                        tah = Tah((radek, sloupec), (radek_do, sloupec_do), figurka)
                        if not tah.over_platnost(docasna_plocha):
                            continue
                        nova_mrizka = self.simulate_move(tah)
                        if not self.check_sach(barva, nova_mrizka):
                            return True
        return False

    def _barva_na_tahu(self):
        """Barva hráče, který je nyní na tahu - opak barvy figurky z
        posledního tahu (self.tah)."""
        if self.tah is None:
            return 1   # na začátku partie je na tahu bílý
        return -self.tah.figurka.barva

    @property
    def check_mat(self) -> bool:
        barva = self._barva_na_tahu()
        return self.check_sach(barva) and not self._existuje_tah_bez_sachu(barva)

    @property
    def check_pat(self) -> bool:
        barva = self._barva_na_tahu()
        return (not self.check_sach(barva)) and not self._existuje_tah_bez_sachu(barva)
