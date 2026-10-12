class View:
    def vykresli(self, herni_deska):
        """herni_deska = hra.plocha.herni_deska, 8x8 seznam Figurka/None"""
        ...

    def oznam_stav(self, stav: int):
        """stav = GameManager.get_stav(): 0=probíhá, 1=šach, 2=mat, 3=pat"""