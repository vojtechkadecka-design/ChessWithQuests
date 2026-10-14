SYMBOLY_SLOUPCU = "abcdefgh"


class View:
    """Stará se jen o zobrazení stavu hry a čtení vstupu od uživatele.
    Nikdy sám nevolá žádnou metodu, která by měnila stav GameManageru -
    o to se stará výhradně Controller."""

    def vykresli_desku(self, herni_deska):
        print()
        for radek in range(7, -1, -1):
            radky = []
            for sloupec in range(8):
                figurka = herni_deska[radek][sloupec]
                radky.append(figurka.symbol() if figurka else ".")
            print(radek + 1, " ".join(radky))
        print("  " + " ".join(SYMBOLY_SLOUPCU))
        print()

    def vypis_stav(self, stav: int, barva_na_tahu: int) -> None:
        """stav podle Controller.stav_hry(): 0=probíhá, 1=šach, 2=mat, 3=pat."""
        if stav == 2:
            vyhral = "Černý" if barva_na_tahu == 1 else "Bílý"
            print(f"Šach mat! Vyhrál {vyhral}.")
        elif stav == 3:
            print("Pat - remíza.")
        elif stav == 1:
            hrac = "Bílý" if barva_na_tahu == 1 else "Černý"
            print(f"{hrac} je v šachu!")

    def vyzvi_k_tahu(self, barva_na_tahu: int) -> str:
        hrac = "Bílý" if barva_na_tahu == 1 else "Černý"
        return input(f"{hrac} hraje (např. 'e2 e4', 'konec' pro ukončení): ").strip()

    def oznam_chybu(self, zprava: str) -> None:
        print(zprava)

    @staticmethod
    def zapis_na_souradnice(zapis: str):
        """Převede např. 'e2' na (radek, sloupec) = (1, 4)."""
        sloupec = SYMBOLY_SLOUPCU.index(zapis[0])
        radek = int(zapis[1]) - 1
        return (radek, sloupec)
