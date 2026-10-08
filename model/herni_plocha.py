from model.figurka import Vez, Kun, Strelec, Dama, Kral, Pesak


class HerniPlocha:
    def __init__(self):
        self.rozmery = (8, 8)
        self.herni_deska = [[None for _ in range(8)] for _ in range(8)]
        self.vyhozene_figurky_b = []   # vyhozené bílé figurky (barva 1)
        self.vyhozene_figurky_c = []   # vyhozené černé figurky (barva -1)

        # výchozí rozestavení - v diagramu není samostatná metoda, takže je
        # součástí konstruktoru stejně jako samotný atribut herni_deska
        rad = [Vez, Kun, Strelec, Dama, Kral, Strelec, Kun, Vez]
        for sloupec, trida in enumerate(rad):
            self.herni_deska[0][sloupec] = trida(1)
            self.herni_deska[7][sloupec] = trida(-1)
        for sloupec in range(8):
            self.herni_deska[1][sloupec] = Pesak(1)
            self.herni_deska[6][sloupec] = Pesak(-1)

    def vrat_obsah(self, souradnice):
        """Vrátí figurku na daných souřadnicích, nebo None (prázdné pole/mimo desku)."""
        radek, sloupec = souradnice
        if not (0 <= radek < self.rozmery[0] and 0 <= sloupec < self.rozmery[1]):
            return None
        return self.herni_deska[radek][sloupec]

    def posun_figurky(self, tah) -> bool:
        """Provede tah. Pokud je cílové pole obsazené soupeřem, deleguje na nahrad_figurku."""
        radek_z, sloupec_z = tah.vychozi_pozice
        radek_do, sloupec_do = tah.cilova_pozice

        figurka = self.herni_deska[radek_z][sloupec_z]
        if figurka is None:
            return False
        if self.herni_deska[radek_do][sloupec_do] is not None:
            return self.nahrad_figurku(figurka, tah)

        self.herni_deska[radek_do][sloupec_do] = figurka
        self.herni_deska[radek_z][sloupec_z] = None
        return True

    def nahrad_figurku(self, figurka, tah) -> bool:
        """Vyhodí soupeřovu figurku z cílového pole a nahradí ji figurkou 'figurka' (braní)."""
        radek_z, sloupec_z = tah.vychozi_pozice
        radek_do, sloupec_do = tah.cilova_pozice

        vyhozena = self.herni_deska[radek_do][sloupec_do]
        if vyhozena is None or vyhozena.barva == figurka.barva:
            return False

        if vyhozena.barva == 1:
            self.vyhozene_figurky_b.append(vyhozena)
        else:
            self.vyhozene_figurky_c.append(vyhozena)

        self.herni_deska[radek_do][sloupec_do] = figurka
        self.herni_deska[radek_z][sloupec_z] = None
        return True
