class GameLogger:
    def __init__(self):
        self.soubor = None

    def vytvor_soubor(self, nazev: str) -> None:
        self.soubor = nazev
        with open(self.soubor, "w", encoding="utf-8") as f:
            f.write("Zápis partie\n")

    def uloz_tah(self, tah) -> None:
        if self.soubor is None:
            self.vytvor_soubor("partie.log")
        zapis = f"{tah.figurka.nazev} {tah.vychozi_pozice} -> {tah.cilova_pozice}\n"
        with open(self.soubor, "a", encoding="utf-8") as f:
            f.write(zapis)
