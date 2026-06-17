class Figurka:
    def __init__(self):
        self.nazev = ""
        self.barva = int #-1 ,nebo 1
        self.vektor = [] #pohybový vektor
        self.vektor_utok = [] #útočný vektor
        self.skok = False

class Dama(Figurka):
    def __init__(self):
        self.nazev = "Dáma"
        pass
    def __str__(self):
        pass

class Kral(Figurka):
    def __init__(self):
        self.nazev = "Král"
        self.vektor = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.vektor_utok = self.vektor
    def __str__(self):
        pass

class Pesak(Figurka):
    def __init__(self):
        self.nazev = "Pěšák"
        self.vektor = [(0,1)] * self.barva
        self.vektor_utok = [(1,1),(-1,1)] * self.barva
    def __str__(self):
        pass

class Kun(Figurka):
    def __init__(self):
        self.nazev = "Kůň"
        self.vektor = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
        self.vektor_utok = self.vektor
        self.skok = True
    def __str__(self):
        pass

class Vez(Figurka):
    def __init__(self):
        self.nazev = "Věž"
        pass
    def __str__(self):
        pass

class Strelec(Figurka):
    def __init__(self):
        self.nazev = "Střelec"
        pass
    def __str__(self):
        pass