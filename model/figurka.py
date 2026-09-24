class Figurka:
    def __init__(self):
        self.nazev = ""
        self.barva = int #-1 ,nebo 1
        self.vektor = [] #pohybový vektor
        self.vektor_utok = [] #útočný vektor
        self.skok = False

    def _nasobky(smery, max_kroku=7):   #Ke každému směru vytvoří vektory o 1 až max_kroku polí.
        vysledek = []   #pro začátek prázdný seznam
        for radek, sloupec in smery:  # pro každý směr
            for k in range(1, max_kroku + 1):  # pro k = 1, 2, ..., 7
                vysledek.append((radek * k, sloupec * k))   #vynásobí směrový vektor všemi možnými kroky (takže až 7krát)
        return vysledek
    SMERY_VEZ = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    SMERY_STRELEC = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
#obecné pohybové vektory, které budou násobeny počtem kroků

class Dama(Figurka):
    def __init__(self):
        super().__init__()
        self.nazev = "Dáma"
        self.vektor = _nasobky(SMERY_VEZ + SMERY_STRELEC)   # věž + střelec
        self.vektor_utok = self.vektor

    def __str__(self):
        return self.nazev

class Kral(Figurka):
    def __init__(self):
        self.nazev = "Král"
        self.vektor = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.vektor_utok = self.vektor
    def __str__(self):
        return self.nazev

class Pesak(Figurka):
    def __init__(self):
        self.nazev = "Pěšák"
        self.vektor = [(0,1)] * self.barva
        self.vektor_utok = [(1,1),(-1,1)] * self.barva
    def __str__(self):
        return self.nazev

class Kun(Figurka):
    def __init__(self):
        self.nazev = "Kůň"
        self.vektor = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
        self.vektor_utok = self.vektor
        self.skok = True
    def __str__(self):
        return self.nazev

class Vez(Figurka):
    def __init__(self):
        super().__init__()
        self.nazev = "Věž"
        self.vektor = _nasobky(SMERY_VEZ)
        self.vektor_utok = self.vektor

    def __str__(self):
        return self.nazev

class Strelec(Figurka):
    def __init__(self):
        super().__init__()
        self.nazev = "Střelec"
        self.vektor = _nasobky(SMERY_STRELEC)
        self.vektor_utok = self.vektor

    def __str__(self):
        return self.nazev

    #Vektory dálkově pohybujících figurek (dáma, věž, střelec) jakkoliv nepočítají s tím, že se může na cestě nacházet obstrukce, nýbrž jenom určují maximální pohyb k okraji herní plochy