class Uzivatel:
    def __init__(self, uzivatelske_jmeno, jmeno="", email="", elo=1000):
        self.uzivatelske_jmeno = uzivatelske_jmeno
        self.jmeno = jmeno
        self.email = email
        self.elo = elo
        self.splnene_kwesty = []   # systém questů není součástí tohoto zadání

    def pridej_quest(self, quest):
        self.splnene_kwesty.append(quest)
