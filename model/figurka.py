class Figurka:
    def __init__(self):
        self.barva = int #-1 a 1
        self.vektor = [] #pohybový vektor
        self.vektor_utok = [] #útočný vektor
        self.skok = False

class Dama(Figurka):
    def __init__(self):
        pass
    def __str__(self):
        pass

class Kral(Figurka):
    def __init__(self):
        self.vektor = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.vektor_utok = self.vektor
    def __str__(self):
        pass

class Pesak(Figurka):
    def __init__(self):
        self.vektor = [(0,1)] * self.barva
        self.vektor_utok = [(1,1),(-1,1)] * self.barva
    def __str__(self):
        pass

class Kun(Figurka):
    def __init__(self):
        self.vektor = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
        self.vektor_utok = self.vektor
        self.skok = True
    def __str__(self):
        pass

class Vez(Figurka):
    def __init__(self):
        pass
    def __str__(self):
        pass

class Strelec(Figurka):
    def __init__(self):
        pass
    def __str__(self):
        pass