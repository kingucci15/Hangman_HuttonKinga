import os


def obtine_vocale():
    # folosim valorile ASCII pentru a genera lista de vocale
    return [chr(i) for i in [65, 69, 73, 79, 85]]  # A, E, I, O, U

def obtine_consoane():
    # Folosim coduri ASCII pentru a genera consoanele
    return [chr(i) for i in [78, 82, 84, 83, 76, 67, 68, 77, 80, 86, 70, 90, 66, 71, 72]]  # N, R, T, etc.

# funcție pentru incarcarea datelor despre cuvinte dintr-un fisier text
def preia_cuvintele(fisier_de_intrare):
    lista_de_cuvinte = []

    # deschidem si citim fisierul linie cu linie
    with open(fisier_de_intrare, 'r', encoding='utf-8') as f:
        for linie in f:
            # eliminam spatiile goale si impartim linia pe baza separatorului ';'
            parti = linie.strip().split(';')
            cod, vizibil, intreg = parti
            # aslvam datele cuvantului sub forma unui dictionar
            lista_de_cuvinte.append({'cod': cod, 'vizibil': vizibil, 'intreg': intreg})

    return lista_de_cuvinte

# functie pentru verificarea daca sa ignoram o anumita pozitie
def trebuie_ignorata_pozitia(index, tip_litera):
    if tip_litera == 'vocala':
        return index % 2 == 0  # ignoram pozitiile pare pentru vocale
    elif tip_litera == 'consoana':
        return index % 3 == 0  # ignoram pozitiile divizibile cu 3 pentru consoane
    return False  # implicit, nu ignoram alte tipuri de litere

# functie care incearca sa completeze cuvantul ascuns
def ghiceste_cuvantul(cuvant_partial, cuvant_complet):
    vocale = obtine_vocale()  # obtinem lista de vocale folosind functia
    consoane = obtine_consoane()  # obtinem lista de consoane folosind functia

    numar_incercari = 0  # contor pentru numarul total de incercari
    cuvant_curent = list(cuvant_partial)  # convertim cuvantul partial intr-o lista de caractere
    litere_gasite = set()  # set pentru a stoca literele deja ghicite

    # incercam sa ghicim vocalele in interiorul cuvantului
    for vocala in vocale:
        if vocala not in litere_gasite:
            for i in range(1, len(cuvant_complet) - 1):
                if cuvant_complet[i].upper() == vocala and cuvant_partial[i] == '*':
                    if trebuie_ignorata_pozitia(i, 'vocala'):
                        continue
                    cuvant_curent[i] = vocala
                    litere_gasite.add(vocala)
                    numar_incercari += 1  # creștem contorul de incercari

    # incercam sa ghicim consoanele, dar folosim aceeasi functie pentru ignorarea pozitiilor
    for consoana in consoane:
        if consoana not in litere_gasite:
            for i in range(1, len(cuvant_complet) - 1):
                if cuvant_complet[i].upper() == consoana and cuvant_partial[i] == '*':
                    if trebuie_ignorata_pozitia(i, 'consoana'):
                        continue
                    cuvant_curent[i] = consoana
                    litere_gasite.add(consoana)
                    numar_incercari += 1

    # inlocuim toate caracterele ascunse ramase (stelutele) cu literele corecte
    for i in range(len(cuvant_curent)):
        if cuvant_curent[i] == '*':
            cuvant_curent[i] = cuvant_complet[i].upper()

    # Returnam cuvantul completat si numarul de incercari
    return ''.join(cuvant_curent), numar_incercari

# Functia principala
def incepe_ghicirea():
    # incercam datele despre cuvinte din fisierul cu cuvinte de verificat
    cuvinte_de_jucat = preia_cuvintele('cuvinte_de_verificat.txt')
    incercari_totale = 0  # variabila pentru numarul total de incercari

    print("-Ghicirea cuvintelor a inceput!-")

    for joc in cuvinte_de_jucat:
        cuvant_final, incercari = ghiceste_cuvantul(joc['vizibil'], joc['intreg'])
        incercari_totale += incercari  # adaugam incercarile pentru acest cuvant la total

        # afisam rezultatele într-un format mai descriptiv si detaliat
        print("--------------------------------------------")
        print(f"Cod joc: {joc['cod']}")
        print(f"Cuvant completat: {cuvant_final}")
        print(f"Numar de incercari efectuate: {incercari}")
        print("--------------------------------------------")

    # La final, afisam raportul cu rezultatele globale
    print("-Raport Jocului Hangman- ")
    print(f"Total incercari pentru toate cuvintele: {incercari_totale}")

    if incercari_totale > 1200:
        print("Avertisment: ati depașit limita de 1200 de încercari!")
    else:
        print("Succes! Toate cuvintele au fost ghicite in mai putin de 1200 incercari.")

# pornim programul daca este rulat direct
if __name__ == "__main__":
    incepe_ghicirea()
