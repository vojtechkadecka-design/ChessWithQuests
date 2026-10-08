class Hrac:
    def __init__(self, barva, uzivatel):
        self.barva = barva          # 1 nebo -1
        self.uzivatel = uzivatel

    def getEloRating(self) -> int:
        return self.uzivatel.elo
