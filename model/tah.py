from model.figurka import Pesak, Dama


class Tah:
    def __init__(self, vychozi_pozice, cilova_pozice, figurka, typ_tahu="normal"):
        self.vychozi_pozice = vychozi_pozice
        self.cilova_pozice = cilova_pozice
        self.figurka = figurka
        self.typ_tahu = typ_tahu

    def over_platnost(self, herni_plocha) -> bool:
        """Geometrická a obsazenostní platnost tahu (bez ohledu na to, zda by
        tah nechal vlastního krále v šachu - to řeší RevizorTahu/GameManager)."""
        if not (self._v_rozmerech(self.vychozi_pozice, herni_plocha.rozmery)
                and self._v_rozmerech(self.cilova_pozice, herni_plocha.rozmery)):
            return False

        na_startu = herni_plocha.vrat_obsah(self.vychozi_pozice)
        if na_startu is None or na_startu is not self.figurka:
            return False

        na_cili = herni_plocha.vrat_obsah(self.cilova_pozice)
        if na_cili is not None and na_cili.barva == self.figurka.barva:
            return False

        pro_utok = na_cili is not None   # tah na obsazené pole = braní
        return self._geometricky_platny(herni_plocha.herni_deska, pro_utok)

    def proved_tah(self, herni_plocha) -> None:
        """Provede tah na herní ploše (předpokládá, že over_platnost již vrátilo True)."""
        herni_plocha.posun_figurky(self)
        self._promen_pokud_na_konci(herni_plocha)

    # --- soukromé pomocné metody (nejsou v diagramu, jen rozpadávají
    #     over_platnost na menší kousky) ---

    @staticmethod
    def _v_rozmerech(pozice, rozmery):
        radek, sloupec = pozice
        return 0 <= radek < rozmery[0] and 0 <= sloupec < rozmery[1]

    def _cesta_volna(self, herni_deska):
        """Zkontroluje, že všechna pole mezi vychozi_pozice a cilova_pozice
        (výlučně) jsou prázdná."""
        radek_z, sloupec_z = self.vychozi_pozice
        radek_do, sloupec_do = self.cilova_pozice
        dr = radek_do - radek_z
        ds = sloupec_do - sloupec_z
        kroku = max(abs(dr), abs(ds))
        smer_r = (dr // kroku) if dr != 0 else 0
        smer_s = (ds // kroku) if ds != 0 else 0

        for k in range(1, kroku):
            r = radek_z + smer_r * k
            s = sloupec_z + smer_s * k
            if herni_deska[r][s] is not None:
                return False
        return True

    def _geometricky_platny(self, herni_deska, pro_utok):
        """pro_utok=True  -> ověřuje se útočný dosah (figurka.vektor_utok)
        pro_utok=False -> ověřuje se klasický tah (figurka.vektor)"""
        if isinstance(self.figurka, Pesak):
            return self._pesak_platny(herni_deska, pro_utok)

        radek_z, sloupec_z = self.vychozi_pozice
        radek_do, sloupec_do = self.cilova_pozice
        dr = radek_do - radek_z
        ds = sloupec_do - sloupec_z

        vektory = self.figurka.vektor_utok if pro_utok else self.figurka.vektor
        if (dr, ds) not in vektory:
            return False

        if not self.figurka.skok and not self._cesta_volna(herni_deska):
            return False

        return True

    def _pesak_platny(self, herni_deska, pro_utok):
        radek_z, sloupec_z = self.vychozi_pozice
        radek_do, sloupec_do = self.cilova_pozice
        dr = radek_do - radek_z
        ds = sloupec_do - sloupec_z
        b = self.figurka.barva

        if pro_utok:
            # pro zjištění, zda pěšák útočí na dané pole (kvůli šachu) - vždy diagonála
            return (dr, ds) in [(sm_dr * b, sm_ds) for sm_dr, sm_ds in self.figurka.vektor_utok]

        # braní (diagonála) - cíl musí být obsazený soupeřem
        if (dr, ds) in [(sm_dr * b, sm_ds) for sm_dr, sm_ds in self.figurka.vektor_utok]:
            return herni_deska[radek_do][sloupec_do] is not None

        # tah o jedno pole dopředu - cíl musí být prázdný
        if (dr, ds) == (1 * b, 0):
            return herni_deska[radek_do][sloupec_do] is None

        # tah o dvě pole dopředu - jen ze startovní řady, cesta i cíl prázdné
        if (dr, ds) == (2 * b, 0):
            start_rada = 1 if b == 1 else 6
            if radek_z != start_rada:
                return False
            mezi_radek = radek_z + b
            return (herni_deska[mezi_radek][sloupec_z] is None
                    and herni_deska[radek_do][sloupec_do] is None)

        return False

    def _promen_pokud_na_konci(self, herni_plocha):
        """Automatická proměna pěšáka na dámu při dosažení poslední řady."""
        radek_do, sloupec_do = self.cilova_pozice
        figurka = herni_plocha.vrat_obsah(self.cilova_pozice)
        if isinstance(figurka, Pesak):
            posledni_rada = 7 if figurka.barva == 1 else 0
            if radek_do == posledni_rada:
                herni_plocha.herni_deska[radek_do][sloupec_do] = Dama(figurka.barva)
