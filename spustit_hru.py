from Controller.controller import Controller
from View.view import View


def main():
    controller = Controller()
    view = View()

    while True:
        view.vykresli_desku(controller.herni_deska())

        stav = controller.stav_hry()
        barva = controller.hrac_na_tahu().barva
        view.vypis_stav(stav, barva)
        if stav in (2, 3):   # mat nebo pat
            break

        zadani = view.vyzvi_k_tahu(barva)
        if zadani.lower() in ("konec", "exit", "quit"):
            break

        try:
            z_str, do_str = zadani.split()
            start = view.zapis_na_souradnice(z_str)
            cil = view.zapis_na_souradnice(do_str)
        except (ValueError, IndexError):
            view.oznam_chybu("Neplatný zápis tahu, zkus např. 'e2 e4'.")
            continue

        if not controller.zpracuj_tah(start, cil):
            view.oznam_chybu("Neplatný tah, zkus to znovu.")


if __name__ == "__main__":
    main()
