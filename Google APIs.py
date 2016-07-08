'''Deel 1: Zoek de website van een praktijk zodat dit in de database gezet kan worden.'''

import urllib.request, urllib.response
import urllib
import json
# import csv

'''
.. function:: telefoonnummerBewerken(nummer)
   De telefoonnummers in de aangeleverde Vektis datasets hebben streepjes. Google kan niet
   goed zoeken met telefoonnummers met streepjes, dus deze functie maakt het een nummer.
   :param nummer: telefoonnummer met streepje.
   :returns: telefoonnummer zonder streepje
'''
def telefoonnummerBewerken(nummer):
    if len(nummer) > 5:
        if nummer[2] == '-':
            nieuwNummer = nummer[0:2] + nummer[3:]
            
        elif nummer[3] == '-':
            nieuwNummer = nummer[0:3] + nummer[4:]
            
        elif nummer[4] == '-':
            nieuwNummer = nummer[0:4] + nummer[5:]
        else:
            nieuwNummer = nummer
    else:
        nieuwNummer = nummer
    return nieuwNummer
         

'''
.. function:: zoekPraktijk(nummer, naam)
   De koppeltabel wordt gemaakt door beide nummertypes in één koppellijst te zetten.
   :param lst1: lijst met zorgverlenernummers.
   :param lst2: lijst met praktijknummers
   :returns: de gevonden URL, of een bericht dat er geen URL gevonden is
'''
def zoekPraktijk(nummer, naam):
    
    nummerAangepast = telefoonnummerBewerken(nummer)
    zoekTerm = nummerAangepast + ' ' + naam
    codeerdeTerm = urllib.parse.quote(zoekTerm, safe='') #de zoekterm wordt veranderd zodat google het kan lezen
    
    APIKey = 'AIzaSyCenzxlkgjkItijd8x0AseTh10hYor-L8I'
    cx = '004386439249891552984:kzfpgdjn5uy' #domein zoekmachine, ingesteld op independer.nl
    
    url = 'https://www.googleapis.com/customsearch/v1?key=' + APIKey + '&cx=' + cx + '&q=' + codeerdeTerm
    
    
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
    ruweData = urllib.request.urlopen(request).read()
    
    data = json.loads(ruweData.decode('utf-8')) #geeft de zoekpagine terug in een speciale vorm
    
    if data['searchInformation']['totalResults'] == '1':
       
       resultaten = list(data.values())[3] #stukje waarin de resultaten met daarin de links 
       print(resultaten)
       link = resultaten[0]['link'] #haalt eerste link op uit de resultaten  
       return link
    else:
          return 'niet gevonden'
    
    
'''
.. function:: zoekPraktijk3(query)
   De Google Knowledge Graph API wordt aangeroepen, er wordt gezocht op de query.
   De resultaten worden gefilterd op URLs.
   :param query: De query waarmee gezocht wordt. Dit bestaat uit een naam van een praktijk 
   en de plaats.
   :returns: de gevonden URL, of een bericht dat er geen URL gevonden is
'''
def zoekPraktijk3(query):
    
    api_key = 'AIzaSyC8-TpYB8BnbpdQc1qiCMGtydu40WLseCI'
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    
    urls = []
    if len(response['itemListElement']) > 0:
        
        for element in response['itemListElement']:
            if 'url' in element['result']:
                urls.append(element['result']['url'])
            if urls == []:
                urls.append('geen url bekend')
    else:
        return 'Onbekend' 
    
    return urls
    
## Deze code importeert het csv bestand in de directory. Echter werkt het 
## importeren alleen binnen de Python console, terwijl gebruik van de iPython console
## nodig is om de database bij te werken. Daarom is er voor gekozen om binnen de
## Spyder 'file explorer' de benodigde csv bestanden te importeren.
'''f = open('vektis_agb_zorgverlener.csv', 'r', encoding = 'UTF-8')
csvreader = csv.reader(f)'''

'''
.. function:: naamVullen()
   Informatie uit de dataset met namen van zorgverleners wordt gebruikt om de voorletters, tussenvoegsels
   en achternamen van zorgverleners in een nieuwe lijst te zetten. Eventuele onnodige spaties
   worden verwijderd.
'''
def naamVullen():   
    for x in range(1, len(Vektis2csv)): #Vektis2csv is vektis_agb_zorgverlener.csv
        achternaam = str(Vektis2csv[x][4])
     
        voorletter = str(Vektis2csv[x][5])
      
        tussenvoegsel = str(Vektis2csv[x][6])
        
        
       
        if voorletter == '(null)' and tussenvoegsel == '(null)' and achternaam != '(null)':
            namen.append(achternaam)
        elif voorletter == '(null)' and tussenvoegsel != '(null)' and achternaam != '(null)':
            namen.append(tussenvoegsel + ' ' + achternaam)
        elif  voorletter != '(null)' and tussenvoegsel == '(null)' and achternaam != '(null)':
            namen.append(voorletter + ' ' + achternaam)
        elif achternaam == '(null)':
            namen.append('')
        else:
            namen.append(voorletter + ' ' + tussenvoegsel + ' ' + achternaam)
 
'''
.. function:: vullen(plekDataSet, array)
   Er wordt informatie uit een bepaalde rij in de Vektis dataset gehaald, en er 
   wordt een nieuwe lijst gevuld met de informatie.
'''            
def vullen(plekDataSet, array):
    for x in range(1, len(Vektis2csv)):
        item = str(Vektis2csv[x][plekDataSet])
        if item != '(null)':
            array.append(item)

#de benodigde variabelen worden aangemaakt.
namen = [0]
telefoonnummers = [0]
plaatsNamen = [0]

vullen(14 ,telefoonnummers)
vullen(13, plaatsNamen)
naamVullen()
websiteHuisartsen = [0] 
 

''' Hiermee wordt de Google Custom Search API aangeroepen met de functie zoekPraktijk,
 er wordt gezocht op telefoonnummer en namen. '''
for x in range(1, len(Vektis2csv)):      
   websiteHuisartsen.append(zoekPraktijk(telefoonnummers[x], namen[x]))
   
''' Hiermee wordt de Google Knowledge Graph API aangeroepen met de functie zoekPraktijk3,
 er wordt gezocht op naam van de praktijk en plaatsnaam. '''
for x in range(1, len(Vektis2csv)):
   websiteHuisartsen.append(zoekPraktijk3(namen[x] + ' ' + plaatsNamen[x]))
