class Timer:
    """Jednoduchý časovač partie. Index v cas_hrac odpovídá indexu
    v GameManager.hraci (0 = bílý, 1 = černý)."""

    def __init__(self, pocatecni_cas=600):
        self.pocatecni_cas = pocatecni_cas
        self.cas_hrac = [pocatecni_cas, pocatecni_cas]

    def nuluj_cas(self) -> None:
        self.cas_hrac = [self.pocatecni_cas, self.pocatecni_cas]

    def pocitej_cas(self, hrac: int) -> None:
        """Odečte jednu sekundu z času hráče s daným indexem."""
        if 0 <= hrac < len(self.cas_hrac) and self.cas_hrac[hrac] > 0:
            self.cas_hrac[hrac] -= 1
