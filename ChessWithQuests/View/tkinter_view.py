import tkinter as tk

VELIKOST_POLE = 70

# mapování ASCII symbolu z Figurka.symbol() (K Q R B N P / k q r b n p)
# na unicode šachové symboly pro hezčí vykreslení
UNICODE_FIGURKY = {
    "K": "\u2654", "Q": "\u2655", "R": "\u2656",
    "B": "\u2657", "N": "\u2658", "P": "\u2659",
    "k": "\u265A", "q": "\u265B", "r": "\u265C",
    "b": "\u265D", "n": "\u265E", "p": "\u265F",
}

SVETLE_POLE = "#f0d9b5"
TMAVE_POLE = "#b58863"
BARVA_VYBER = "#829769"
BARVA_MOZNY_TAH = "#f6f669"


def souradnice_z_pixelu(x, y, velikost_pole=VELIKOST_POLE):
    """Převede pixelové souřadnice kliknutí na (radek, sloupec) šachovnice.
    V Tkinteru roste y směrem dolů, ale radek 0 je u nás spodní řada (bílí),
    proto je potřeba řádek obrátit."""
    sloupec = x // velikost_pole
    radek = 7 - (y // velikost_pole)
    return int(radek), int(sloupec)


def pixel_z_souradnic(radek, sloupec, velikost_pole=VELIKOST_POLE):
    """Opačný převod - levý horní roh pole (radek, sloupec) v pixelech."""
    x0 = sloupec * velikost_pole
    y0 = (7 - radek) * velikost_pole
    return x0, y0


def je_svetle_pole(radek, sloupec):
    return (radek + sloupec) % 2 == 1


class TkinterView:
    """Grafické zobrazení šachovnice přes Tkinter. Místo psaní tahu do
    konzole (viz View/view.py) se klikne na výchozí a pak na cílové pole -
    jinak funguje úplně stejně: pouze čte data z Controlleru a volá jeho
    zpracuj_tah(), samo žádný stav hry neupravuje."""

    def __init__(self, controller):
        self.controller = controller
        self.vybrane_pole = None   # (radek, sloupec) prvně kliknutého pole, nebo None

        self.okno = tk.Tk()
        self.okno.title("Šachy")

        self.platno = tk.Canvas(self.okno, width=8 * VELIKOST_POLE, height=8 * VELIKOST_POLE)
        self.platno.pack()
        self.platno.bind("<Button-1>", self._klik)

        self.stavovy_radek = tk.Label(self.okno, text="", font=("Arial", 14))
        self.stavovy_radek.pack(pady=6)

        self._prekresli()

    def spustit(self) -> None:
        """Spustí hlavní smyčku okna - blokuje, dokud se okno nezavře."""
        self.okno.mainloop()

    def _klik(self, event) -> None:
        radek, sloupec = souradnice_z_pixelu(event.x, event.y)
        if not (0 <= radek < 8 and 0 <= sloupec < 8):
            return

        if self.vybrane_pole is None:
            figurka = self.controller.herni_deska()[radek][sloupec]
            if figurka is not None:
                self.vybrane_pole = (radek, sloupec)
        else:
            vychozi_pozice = self.vybrane_pole
            self.vybrane_pole = None
            uspech = self.controller.zpracuj_tah(vychozi_pozice, (radek, sloupec))
            if not uspech:
                self.stavovy_radek.config(text="Neplatný tah, zkus to znovu.")

        self._prekresli()

    def _prekresli(self) -> None:
        self.platno.delete("all")
        herni_deska = self.controller.herni_deska()

        for radek in range(8):
            for sloupec in range(8):
                x0, y0 = pixel_z_souradnic(radek, sloupec)
                x1, y1 = x0 + VELIKOST_POLE, y0 + VELIKOST_POLE

                if self.vybrane_pole == (radek, sloupec):
                    barva_pole = BARVA_VYBER
                else:
                    barva_pole = SVETLE_POLE if je_svetle_pole(radek, sloupec) else TMAVE_POLE

                self.platno.create_rectangle(x0, y0, x1, y1, fill=barva_pole, outline="")

                figurka = herni_deska[radek][sloupec]
                if figurka is not None:
                    znak = UNICODE_FIGURKY.get(figurka.symbol(), figurka.symbol())
                    self.platno.create_text(x0 + VELIKOST_POLE / 2, y0 + VELIKOST_POLE / 2,
                                             text=znak, font=("Arial", 36))

        self._aktualizuj_stavovy_radek()

    def _aktualizuj_stavovy_radek(self) -> None:
        if self.vybrane_pole is not None:
            return   # uprostřed výběru tahu nic nepřepisujeme

        stav = self.controller.stav_hry()
        barva = self.controller.hrac_na_tahu().barva
        hrac = "Bílý" if barva == 1 else "Černý"

        if stav == 2:   # mat
            vyhral = "Černý" if barva == 1 else "Bílý"
            self.stavovy_radek.config(text=f"Šach mat! Vyhrál {vyhral}.")
        elif stav == 3:   # pat
            self.stavovy_radek.config(text="Pat - remíza.")
        elif stav == 1:   # šach
            self.stavovy_radek.config(text=f"{hrac} je v šachu! Táhne {hrac}.")
        else:
            self.stavovy_radek.config(text=f"Táhne: {hrac}")
