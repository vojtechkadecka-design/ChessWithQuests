"""
Základní třída Figurka a všechny konkrétní šachové figurky.

Souřadnice na desce jsou dvojice (radek, sloupec), 0 až 7.
Barva: 1 = bílý hráč, -1 = černý hráč (podle poznámky v class diagramu).
"""


def _nasobky(smery, max_kroku=7):
    """Ke každému směru vytvoří vektory o 1 až max_kroku polí (pro figurky,
    které se posouvají po přímce o libovolný počet polí)."""
    return [(dr * k, ds * k) for dr, ds in smery for k in range(1, max_kroku + 1)]


SMERY_VEZ = [(0, 1), (0, -1), (1, 0), (-1, 0)]
SMERY_STRELEC = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


class Figurka:
    def __init__(self, barva):
        self.nazev = ""
        self.barva = barva        # 1 nebo -1 podle barvy (týmu)
        self.vektor = []          # pohybový vektor
        self.vektor_utok = []     # útočný vektor
        self.skok = False         # True = může přeskakovat jiné figurky (kůň)

    def __str__(self):
        return self.nazev

    def symbol(self):
        """Jednoznakový symbol pro výpis šachovnice do konzole."""
        znak = self._znak()
        return znak.upper() if self.barva == 1 else znak.lower()

    def _znak(self):
        return "?"


class Kun(Figurka):
    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Kůň"
        self.vektor = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.vektor_utok = self.vektor
        self.skok = True

    def _znak(self):
        return "N"


class Kral(Figurka):
    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Král"
        self.vektor = [(0, 1), (0, -1), (1, 0), (-1, 0),
                       (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.vektor_utok = self.vektor

    def _znak(self):
        return "K"


class Vez(Figurka):
    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Věž"
        self.vektor = _nasobky(SMERY_VEZ)
        self.vektor_utok = self.vektor

    def _znak(self):
        return "R"


class Strelec(Figurka):
    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Střelec"
        self.vektor = _nasobky(SMERY_STRELEC)
        self.vektor_utok = self.vektor

    def _znak(self):
        return "B"


class Dama(Figurka):
    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Dáma"
        self.vektor = _nasobky(SMERY_VEZ + SMERY_STRELEC)
        self.vektor_utok = self.vektor

    def _znak(self):
        return "Q"


class Pesak(Figurka):
    """Pěšák. Vektory jsou definované jako pro bílého hráče (barva = 1) a při
    použití se vynásobí barvou (self.barva)"""

    def __init__(self, barva):
        super().__init__(barva)
        self.nazev = "Pěšák"
        self.vektor = [(1, 0), (2, 0)]          # dopředu 1, nebo ze startu 2 pole
        self.vektor_utok = [(1, 1), (1, -1)]    # braní diagonálně

    def _znak(self):
        return "P"
