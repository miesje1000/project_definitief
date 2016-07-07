'''Deel 1 en 2: Genereer tabellen met gegevens van huisartsen en praktijken. '''

import socket
#import csv

praktijk = []

## Deze code importeert het csv bestand in de directory. Echter werkt het 
## importeren alleen binnen de Python console, terwijl gebruik van de iPython console
## nodig is om de database bij te werken. Daarom is er voor gekozen om binnen de
## Spyder 'file explorer' de benodigde csv bestanden te importeren.
'''f = open('vektis_agb_praktijk.csv', 'r', encoding = 'UTF-8')
csvreader = csv.reader(f)'''

praktijk = []
'''
.. function:: zoekpraktijk(lst)
   Leest het bijgevoegde csv bestand en bekijkt welke rijen als zorgverlenersoort '01' hebben.
   Dat geeft aan dat de rij gegevens over een huisarts bevat.
   De functie slaat deze gevonden rijen in een nieuwe lijst op.
   :param lst: CSV bestand waar de data over praktijken in staat. 
'''
def zoekpraktijk(lst):
    for col in lst:
        if col[2] == int('01'):
            praktijk.append(col)

# Praktijkcsv is de naam van het 'vektis_agb_praktijk.csv' bestand, dat
# met de file explorer geimporteerd is.
zoekpraktijk(praktijkcsv)
## Hier zou het ingelezen csv bestand door de functie zoekpraktijk gebruikt worden.
'''zoekpraktijk(csvreader)
f.close()'''

prNr = []
prNa1 = []
prNa2 = []
prTel = []

''' Voor elke rij in praktijk worden respectievelijk het praktijknummer,
de naam en het telefoonnummer in een aparte lijst opgeslagen.'''
for item in praktijk:
    prNr.append(item[3])
    prNa1.append(item[4])
    prNa2.append(item[5])
    prTel.append(item[6])

pr = []
'''
.. function:: prSamenvoegen(lst1, lst2, lst3, lst4)
   Deze functie voegt vier aparte lijsten samen in één lijst.
   :param lst1: Lijst met praktijknummer, deze informatie wordt in een nieuwe lijst gezet.
   :param lst2: Lijst met naam (deel 1), deze informatie wordt in een nieuwe lijst gezet.
   :param lst3: Lijst met naam (deel 2), deze informatie wordt in een nieuwe lijst gezet.
   :param lst4: Lijst met telefoonnummer, deze informatie wordt in een nieuwe lijst gezet.
'''
def prSamenvoegen(lst1, lst2, lst3, lst4):
       
    for item in lst1:
        pr.append(item)
    for item in lst2:
        pr.append(item)
    for item in lst3:
        pr.append(item)
    for item in lst4:
        pr.append(item)
        
prSamenvoegen(prNr, prNa1, prNa2, prTel)

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

''' De eerste en tweede kolom worden samengevoegd.'''
for item in prSort:
    if item[2] != '(null)':
        item[1] = item[1] + ' ' + item[2]
    item.remove(item[2])
    
'''Lees het bestand met praktijk adressen in.'''

prakAdres = []
## alternatief voor importeren
'''f = open('vektis_agb_praktijk_adres.csv', 'r', encoding = 'UTF-8')
csvreader = csv.reader(f)'''

'''
.. function:: zoekhuisarts(lst)
   Leest het bijgevoegde csv bestand en bekijkt welke rijen als zorgverlenersoort '01' hebben.
   Dat geeft aan dat de rij gegevens over een huisarts bevat.
   De functie slaat deze gevonden rijen in een nieuwe lijst op.
   :param lst: CSV bestand waar de data over praktijken in staat. 
'''
def zoekhuisarts(lst):
    for col in lst:
        if col[2] == int('01'): 
            prakAdres.append(col)

# PraktijkAdrescsv is de naam van het 'vektis_agb_praktijk_adres.csv' bestand, dat
# met de file explorer geimporteerd is.
zoekhuisarts(PraktijkAdrescsv)

'''
.. function:: koppeling(lst1, lst2)
   Voeg het adres toe door middel van het nummer van de praktijk.
   :param lst1: lijst waar de data over praktijken gesorteerd in staat. 
   :param lst2: lijst waar de adresgegevens in staan.
'''
def koppeling(lst1, lst2):

    for item in lst1:
        for ding in lst2:
            if item[0] == ding[3]:
                item.append(ding[5])
                item.append(ding[6])
                item.append(ding[7])
                item.append(ding[8])
                item.append(ding[9])
    
koppeling(prSort, prakAdres)

'''Maak een tabel aan in de database genaamd Praktijken en voeg de 
naam, het telefoonnummer en het adres toe.'''
import sqlite3

db = sqlite3.connect('specialismen_db.sqlite')

#tabel voor Huisartsen aanmaken
cursor = db.cursor()
cursor.execute('''
   CREATE TABLE IF NOT EXISTS Praktijken(id INT PRIMARY KEY, naam TEXT, telnr TEXT, straat TEXT, huisnummer INT, toevoeging TEXT, postcode TEXT, woonplaats TEXT, lat REAL, long REAL, website TEXT)
''')

#data uit haData en adresCor inlezen in tabel Huisartsen
for lst in prSort:
   cursor.execute('''INSERT INTO Praktijken(id, naam, telnr, straat, huisnummer, toevoeging, postcode, woonplaats)
                VALUES(?,?,?,?,?,?,?,?)''', (lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7]))

#wijzigingen opslaan en connectie met db verbreken
db.commit()
cursor.close()

'''Maak lijsten aan om adresgegevens op te slaan en verzamel 
ze in 1 lijst. Met deze lijst kunnen de coordinaten van de praktijken
gezocht worden.'''
prakStraat = []
prakNummer = []
prakToevoeging = []
prakPostcode =[]
prakWoonplaats = []
prAdres=[]

'''
.. function:: adresVerzamelaar(lst)
   Leest de bijgevoegde lijst en vult nieuwe lijsten, waar apart onderdelen van het adres
   in gezet worden.
   :param lst: lijst waar de adresgegevens in staan. 
'''
def adresVerzamelaar(lst):
    for x in lst:
         prakStraat.append(x[5])
         prakNummer.append(x[6]) 
         prakToevoeging.append(x[7])
         prakPostcode.append(x[8])
         prakWoonplaats.append(x[9])     
                
adresVerzamelaar(prakAdres)

'''
.. function:: lijstmaker(lijst1, lijst2, lijst3, lijst4)
   Leest alle aparte lijsten met adresgegevens in en maakt er een overzichtelijke
   nieuwe lijst van.
   :param lijst1: lijst met straatnamen 
   :param lijst2: Lijst met huisnummers.
   :param lijst3: Lijst met postcodes.
   :param lijst4: Lijst met woonplaatsen.
'''
def lijstmaker(lijst1,lijst2,lijst3,lijst4):
    for i in lijst1,lijst2,lijst3,lijst4:
        for item in i:
            prAdres.append(item)

lijstmaker(prakStraat,prakNummer,prakPostcode,prakWoonplaats)

prakAdressort = []
'''
.. function:: adresSort(lijstje)
   Sorteer de lijst met adresgegevens zodat een volledig adres per huisarts als list wordt opgeslagen.
   :param lijstje: lijst met praktijkadressen. 
'''
def adresSort(lijstje):
    for i in range(len(prakAdres)):
        prakAdressort.append(lijstje[i:len(lijstje)+i:len(prakAdres)]) 
      
adresSort(prAdres)

adresCor = []

'''
.. function:: adresGeo(lst)
   Zoek met behulp van de net gemaakte adreslijst (prakAdressort)
   de bijbehorende coordinaten.
   :param lst: Adreslijst. 
'''
def adresGeo(lst):
    from time import sleep
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(500)
    for item in lst:
         location = geolocator.geocode(item, timeout=500)
         if location:
             locatieCor = [location.latitude, location.longitude]
             adresCor.append(locatieCor)
             sleep(1)
         else:
             adresCor.append("onbekend")
             sleep(1)
             
adresGeo(prakAdressort[0:len(prakAdressort)])

praktijkNamenCoordinaten = []

'''
.. function:: prakEnCor(lst1, lst2)
   Voeg de nummers van de praktijken aan de coordinaten toe, 
   zodat deze gekoppeld kunnen worden aan de juiste praktijken
   :param lst1: Lijst met adresgegevens.
   :param lst2: Lijst met gevonden coördinaten.
'''
def prakEnCor(lst1, lst2):
    for item in lst1:
        praktijkNamenCoordinaten.append(item[3])
    for item in lst2:
        praktijkNamenCoordinaten.append(item[0])
    for item in lst2:
        praktijkNamenCoordinaten.append(item[1])

prakEnCor(prakAdres, adresCor)

gesorteerdNummerEnCoordinaten = []

'''
.. function:: corSort(lijstje)
   Sorteer de lijst met coördinaten zodat de coördinaten in dezelfde lijst
   als de praktijkadressen komen.
   :param lijstje: de lijst met nummers van praktijken en coördinaten 
'''
def corSort(lijstje):
    for i in range(len(prakAdres)):
        gesorteerdNummerEnCoordinaten.append(lijstje[i:len(lijstje)+i:len(prakAdres)])
        
corSort(praktijkNamenCoordinaten)

'''Voeg de coordinaten toe aan de praktijken in de database.'''
import sqlite3

db = sqlite3.connect('specialismen_db.sqlite')

#tabel voor Huisartsen aanmaken
cursor = db.cursor()
cursor.execute('''
   CREATE TABLE IF NOT EXISTS Praktijken(id INT PRIMARY KEY, naam TEXT, telnr TEXT, straat TEXT, huisnummer INT, toevoeging TEXT, postcode TEXT, woonplaats TEXT, lat REAL, long REAL, website TEXT)
''')

for lst in gesorteerdNummerEnCoordinaten:
    if lst[1] != 'o' and lst [2] != 'n':
        sql = "update Praktijken set lat = %f, long = %f where id = %d" % (lst[1], lst[2], lst[0])
        cursor.execute(sql)

#wijzigingen opslaan en connectie met db verbreken
db.commit()
cursor.close()
