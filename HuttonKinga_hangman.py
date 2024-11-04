import csv


# definim lista de vocale si consoane
def obtine_vocale():
    # retuneaza vocalele posibile
    return ['A', 'E', 'I', 'O', 'U', 'Ă', 'Î','Â']


def obtine_consoane():
    # returneaza consoanele posibile
    return ['N', 'R', 'T', 'S', 'L', 'C', 'D', 'M', 'P', 'V', 'F', 'Z', 'B', 'G', 'H', 'Ș', 'Ț','J', 'X', 'K']
#cele doua functii sunt folosite pt a verifica daca V sau C apar in cuvantul
#pe care dorim sa ghicim, si alg incearca sa compl literele necunoscute in
#cuvant_partial

# fct principala care incearca sa completeze cuvantul
def completare_cuvant_optimizat(cuvant_partial, cuvant_complet):
    incercari = 0
    cuvant_actual = list(cuvant_partial)  # convertim in lista pt a putea modif individual literele
    litere_ghicite = set(cuvant_partial.replace('*', '').upper())
    # set care retine literele ghicite deja ca sa nu reptam incercarile

    # incearca ghicirea vocalelor
    for litera in obtine_vocale():
        if litera not in litere_ghicite:
            for i in range(len(cuvant_complet)):
                if cuvant_complet[i].upper() == litera and cuvant_partial[i] == '*':
                    cuvant_actual[i] = litera
                    litere_ghicite.add(litera)
                    incercari += 1
#daca vocala curenta nu a fost ghicita deja, funct verifica fiecare poz din
#cuvant_complet
#daca litera din poz resp este vocala curenta si pozitia in cuvant_partial este
#inca * atunci vocala este completata in cuvant_actual
#actualizam setul litere_ghicite cu vocala curenta + contorul de incercari
    # incearca ghicirea consoanelor
    for litera in obtine_consoane():
        if litera not in litere_ghicite:
            for i in range(len(cuvant_complet)):
                if cuvant_complet[i].upper() == litera and cuvant_partial[i] == '*':
                    cuvant_actual[i] = litera
                    litere_ghicite.add(litera)
                    incercari += 1


    return ''.join(cuvant_actual), incercari


# fct princ ce gestioneaza jocul, filename duce catre fisier din care citim
def run_hangman(filename):
    total_incercari = 0
    cuvinte = []
    #fiecare rand este citit si stocat intro lista de dictionare cuvinte

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            cod, partial, complet = row
            cuvinte.append({'cod': cod, 'partial': partial, 'complet': complet})

    # ficare cuvant din lista cuvinte este procesat
    # se extrag valori pt cod partial complet
    # apelam completare_cuvant_optimizat pt a obt cuvantul compl si numarul de inc
    # se aduna la total si afisam rezultatul
    for cuvant in cuvinte:
        cod = cuvant['cod']
        partial = cuvant['partial']
        complet = cuvant['complet']
        cuvant_ghicit, incercari = completare_cuvant_optimizat(partial, complet)
        total_incercari += incercari
        print(f"Jocul: {cod}, Am ghicit: {cuvant_ghicit}, Încercări: {incercari}")

    print(f"Rezultatul de încercări: {total_incercari}")
    if total_incercari > 1200:
        print("Numărul de încercări a depășit limita de 1200.")
    else:
        print("Toate cuvintele au fost găsite cu succes sub limita de 1200 încercări!")


filename = 'cuvinte_de_verificat.txt' 
run_hangman(filename)
