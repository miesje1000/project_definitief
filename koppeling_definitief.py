''' Deel 3: Koppelingstabel. Importeer handmatig de bestanden waarin de zorgverleners staan, 
de praktijken en de koppeling tussen deze twee.'''

#import csv

# Deze code importeert het csv bestand (dat in deze directory is 
# opgenomen) . Echter werkt het importeren alleen binnen de Python console, 
# terwijl gebruik van de iPython consolenodig is om de database bij te werken.
# Daarom is er voor gekozen om binnen de Spyder 'file explorer' de benodigde 
# csv bestanden te importeren.
'''f = open('vektis_agb_zorgverlener.csv', 'r', encoding = 'UTF-8')
csvreader = csv.reader(f)''' 

haData = []

'''
.. function:: zoekhuisarts(lst)
   Leest het bijgevoegde csv bestand en bekijkt welke rijen als zorgverlenersoort '01' hebben.
   Dat geeft aan dat de rij gegevens over een huisarts bevat.
   De functie slaat deze gevonden rijen in een nieuwe lijst op.
   :param lst: CSV bestand waar de data over zorgverleners in staat. 
'''
def zoekhuisarts(lst):
    for col in lst:
        if col[2] == int('01'):
            haData.append(col)

# Tabelcsv is de naam van het 'vektis_agb_zorgverlener.csv' bestand, dat
# met de file explorer geimporteerd is.
zoekhuisarts(tabelcsv)

#alternatieve import
'''zoekhuisarts(csvreader)
f.close()'''

'''Maak van voorletters, tussenvoegsel(s) en achternaam één list.'''
for item in haData:
    if item[6] != '(null)':
        item[4] = item[5] + ' ' + item[6] + ' ' + item[4]
        item.remove(item[5])
        item.remove(item[6])
    else:
        item[4] = item[5] + ' ' + item[4]
        item.remove(item[5])
        item.remove(item[6])

''' Code om csv in source directory te importeren:
f = open('vektis_agb_praktijk.csv', 'r', encoding = 'UTF-8')
csvpraktijk = csv.reader(f)''' 
praktijk = []
'''
.. function:: zoekpraktijk(lst)
   Leest het bijgevoegde csv bestand en bekijkt welke rijen als zorgverlenersoort '01' hebben.
   Dat geeft aan dat de rij gegevens over een huisartsenpraktijk bevat.
   De functie slaat deze gevonden rijen in een nieuwe lijst op.
   :param lst: CSV bestand waar de data over praktijken in staat. 
'''
def zoekpraktijk(lst):
    for col in lst:
        if col[2] == int('01'):
            praktijk.append(col)

zoekpraktijk(praktijkcsv)
# alternatieve import
'''zoekpraktijk(csvreader)
f.close()'''

prNr = []
prNa1 = []
prNa2 = []

''' Er worden drie nieuwe lijsten gevuld met respectievelijk praktijknummer en
naam van de praktijk, die in de lijst met praktijkgegevens te vinden zijn. '''
for item in praktijk:
    prNr.append(item[3])
    prNa1.append(item[4])
    prNa2.append(item[5])

pr = []
'''
.. function:: prSamenvoegen(lst1, lst2, lst3)
   Maakt van de drie lijsten één lijst met praktijknummer en naam.
   :param lst1: lijst met nummer van praktijk (niet telefoonnummer!) 
   :param lst2: lijst met eerste deel van naam
   :param lst3: lijst met tweede deel van naam
'''
def prSamenvoegen(lst1, lst2, lst3):
    for item in lst1:
        pr.append(item)
    for item in lst2:
        pr.append(item)
    for item in lst3:
        pr.append(item)
        
prSamenvoegen(prNr, prNa1, prNa2)

prSort = []

'''
.. function:: praktijkSort(lst)
   Sorteert de lijst met samengevoegde praktijkgegevens zodat er een volledige lijst met
   overzichtelijke gegevens gemaakt kan worden.
   :param lst: lijst met praktijkgegevens
'''
def praktijkSort(lst):
    for i in range(len(praktijk)):
        prSort.append(lst[i:len(pr)+i:len(praktijk)])
        
praktijkSort(pr)

'''De eerste en tweede kolom worden samengevoegd.'''
for item in prSort:
    if item[2] != '(null)':
        item[1] = item[1] + ' ' + item[2]
    item.remove(item[2])

''' Alternatieve code om csv in map te importeren:
f = open('vektis_agb_koppeling_zorgverlener_praktijk.csv', 'r', encoding = 'UTF-8')
csvpraktijk = csv.reader(f)''' 

koppel = []

'''
.. function:: zoekkoppel(lst)
   Leest het bijgevoegde csv bestand en bekijkt welke rijen als zorgverlenersoort '01' hebben.
   Dat geeft aan dat de rij gegevens over een huisarts bevat.
   De functie slaat deze gevonden rijen in een nieuwe lijst op.
   :param lst: lijst waar de zorgverlenernummers en praktijknummers in staan. 
'''
def zoekkoppel(lst):
    for col in lst:
        if col[2] == int('01'):
            koppel.append(col)

zoekkoppel(koppelcsv)
# alternatieve import
'''zoekpraktijk(csvreader)
f.close()'''

kopHa = []
kopPr = []

''' Voor elke rij in de koppeltabel worden de zorgverlenernummers en praktijknummers
in een andere lijst gezet.'''
for item in koppel:
    kopHa.append(item[3])
    kopPr.append(item[4])
    
kopHaPr = []

'''
.. function:: haEnPr(lst1, lst2)
   De koppeltabel wordt gemaakt door beide nummertypes in één koppellijst te zetten.
   :param lst1: lijst met zorgverlenernummers.
   :param lst2: lijst met praktijknummers
'''
def haEnPr(lst1, lst2):
    for item in lst1:
        kopHaPr.append(item)
    for item in lst2:
        kopHaPr.append(item)
        
haEnPr(kopHa, kopPr)

koppelSort = []
'''
.. function:: kopSort(lst)
   Sorteert de lijst met samengevoegde nummers zodat de correcte nummers gekoppeld
   worden.
   :param lst: lijst met zorgverlenernummers en praktijknummers
'''
def kopSort(lst):
    for i in range(len(kopHa)):
        koppelSort.append(lst[i:len(kopHaPr)+i:len(kopHa)])
        
kopSort(kopHaPr)

'''
.. function:: koppeling(lst1, lst2, lst3)
   Vervang in de lijst met koppelingen de nummers van de huisartsen en
   praktijken door de namen van de huisartsen en praktijken.
   :param lst1: lijst met gesorteerde nummers
   :param lst2: lijst met gesorteerde praktijkgegevens
   :param lst3: lijst met huisartsengegevens
'''
def koppeling(lst1, lst2, lst3):
    for item in lst1:
        for obj in lst3:
            if item[0] == obj[2]:
                item[0] = obj[3]
        for ding in lst2:
            if item[1] == ding[0]:
                item[1] = ding[1]
        
koppeling(koppelSort, prSort, haData)

'''Schrijf de gegenereerde data weg naar de specialismendatabase
in een tabel genaamd Huisartsen.'''
import sqlite3

db = sqlite3.connect('specialismen_db.sqlite')

cursor = db.cursor()
cursor.execute('''
   CREATE TABLE IF NOT EXISTS Huisartsen(huisarts TEXT, praktijk TEXT)
''')

for lst in koppelSort:
   cursor.execute('''INSERT INTO Huisartsen(huisarts, praktijk)
                VALUES(?,?)''', (lst[0], lst[1]))

db.commit()
cursor.close()




            




            
