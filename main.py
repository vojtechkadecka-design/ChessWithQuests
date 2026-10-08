from model.uzivatel import Uzivatel
from model.game_manager import GameManager, STAV_MAT, STAV_PAT, STAV_SACH


SYMBOLY_SLOUPCU = "abcdefgh"


def vypis_desku(plocha):
    print()
    for radek in range(7, -1, -1):
        radky = []
        for sloupec in range(8):
            figurka = plocha.herni_deska[radek][sloupec]
            radky.append(figurka.symbol() if figurka else ".")
        print(radek + 1, " ".join(radky))
    print("  " + " ".join(SYMBOLY_SLOUPCU))
    print()


def zapis_na_souradnice(zapis: str):
    """Převede např. 'e2' na (radek, sloupec) = (1, 4)."""
    sloupec = SYMBOLY_SLOUPCU.index(zapis[0])
    radek = int(zapis[1]) - 1
    return (radek, sloupec)


def main():
    bily = Uzivatel("hrac_bily", jmeno="Bílý hráč")
    cerny = Uzivatel("hrac_cerny", jmeno="Černý hráč")
    hra = GameManager(bily, cerny)

    while True:
        vypis_desku(hra.plocha)
        stav = hra.get_stav()
        if stav == STAV_MAT:
            vyhral = "Černý" if hra.aktivni_hrac == 0 else "Bílý"
            print(f"Šach mat! Vyhrál {vyhral}.")
            break
        if stav == STAV_PAT:
            print("Pat - remíza.")
            break
        if stav == STAV_SACH:
            print("Šach!")

        na_tahu = "Bílý" if hra.aktivni_hrac == 0 else "Černý"
        zadani = input(f"{na_tahu} hraje (např. 'e2 e4', 'konec' pro ukončení): ").strip()
        if zadani.lower() in ("konec", "exit", "quit"):
            break

        try:
            z_str, do_str = zadani.split()
            start = zapis_na_souradnice(z_str)
            cil = zapis_na_souradnice(do_str)
        except (ValueError, IndexError):
            print("Neplatný zápis tahu, zkus např. 'e2 e4'.")
            continue

        tah = hra.zacni_tah()
        tah.vychozi_pozice = start
        tah.cilova_pozice = cil
        tah.figurka = hra.plocha.vrat_obsah(start)
        if tah.figurka is None:
            print("Na výchozím poli není žádná figurka.")
            continue

        if not hra.proved_tah(tah):
            print("Neplatný tah, zkus to znovu.")


if __name__ == "__main__":
    main()
