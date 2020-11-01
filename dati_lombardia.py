import json
import matplotlib.pyplot as plt
import numpy as np


def media_su_giorni(date, valori, giorni):
	cumulo_valori = 0.0
	media_valori = []
	giorni_float = float(giorni)
	for i in range(giorni):
		cumulo_valori = cumulo_valori + float(valori[i])
	media_valori.append(cumulo_valori / giorni_float)
	for i in range(giorni, len(date)):
		cumulo_valori = cumulo_valori + float(valori[i] - valori[i - giorni])
		media_valori.append(cumulo_valori / giorni_float)
	return date[giorni - 1:], media_valori

json_file = open('/Users/matteos/Desktop/COVID/COVID-19/dati-json/dpc-covid19-ita-regioni.json')
dati = json.load(json_file)

date = []
nuovi_ricoverati = []
ricoverati_con_sintomi = []
nuove_terapie_intensive = []
terapie_intensive = []
nuovi_ospedalizzati = []
totale_ospedalizzati = []
nuovi_isolamento = []
isolamento_domiciliare = []
totale_positivi = []
variazione_totale_positivi = []
nuovi_positivi = []
nuovi_dimessi_guariti = []
dimessi_guariti = []
nuovi_deceduti = []
deceduti = []
totale_casi = []
tamponi = []
casi_testati = []
percentuale_test_positivi = []

casi_testati_ieri = 0
deceduti_totali_ieri = 0
terapie_intensive_totali_ieri = 0
dimessi_guariti_totali_ieri = 0
ricoverati_totali_ieri = 0
isolamento_totali_ieri = 0
ospedalizzati_totali_ieri = 0

for dato in dati:
	if dato['denominazione_regione'] == 'Lombardia':
		#Totale
	    casi_testati_oggi = dato['casi_testati']
	    nuovi_positivi_oggi = dato['nuovi_positivi']
	    deceduti_totali_oggi = dato['deceduti']
	    terapie_intensive_totali_oggi = dato['terapia_intensiva']
	    dimessi_guariti_totali_oggi = dato['dimessi_guariti']
	    ricoverati_totali_oggi = dato['ricoverati_con_sintomi']
	    isolamento_totali_oggi = dato['isolamento_domiciliare']
	    severi_totali_oggi = dato['totale_ospedalizzati']

	    #Incremento oggi
	    deceduti_oggi = deceduti_totali_oggi - deceduti_totali_ieri
	    terapie_intensive_oggi = terapie_intensive_totali_oggi - terapie_intensive_totali_ieri
	    dimessi_guariti_oggi = dimessi_guariti_totali_oggi - dimessi_guariti_totali_ieri
	    ricoverati_oggi = ricoverati_totali_oggi - ricoverati_totali_ieri
	    isolamento_oggi = isolamento_totali_oggi - isolamento_totali_ieri
	    ospedalizzati_oggi = severi_totali_oggi - ospedalizzati_totali_ieri

	    #Salvataggio di nuovi dati
	    date.append(dato['data'][5:10])
	    nuovi_ricoverati.append(ricoverati_oggi)
	    ricoverati_con_sintomi.append(ricoverati_totali_oggi)
	    nuove_terapie_intensive.append(terapie_intensive_oggi)
	    terapie_intensive.append(terapie_intensive_totali_oggi)
	    nuovi_ospedalizzati.append(ospedalizzati_oggi)
	    totale_ospedalizzati.append(severi_totali_oggi)
	    nuovi_isolamento.append(isolamento_oggi)
	    isolamento_domiciliare.append(isolamento_totali_oggi)
	    totale_positivi.append(dato['totale_positivi'])
	    variazione_totale_positivi.append(dato['variazione_totale_positivi'])
	    nuovi_positivi.append(nuovi_positivi_oggi)
	    nuovi_dimessi_guariti.append(dimessi_guariti_oggi)
	    dimessi_guariti.append(dimessi_guariti_totali_oggi)
	    deceduti.append(deceduti_totali_oggi)
	    nuovi_deceduti.append(deceduti_oggi)
	    totale_casi.append(dato['totale_casi'])
	    tamponi.append(dato['tamponi'])
	    casi_testati.append(casi_testati_oggi)

	    #Calcoli
	    so_float = float(severi_totali_oggi)

	    if ((casi_testati_oggi != None) and (casi_testati_ieri != 0)):
	        nuovi_casi_testati = float((casi_testati_oggi - casi_testati_ieri))
	        if nuovi_casi_testati != 0:
	        	percentuale_test_positivi.append(float(nuovi_positivi_oggi) * 100.0 / nuovi_casi_testati)
	        else:
	        	percentuale_test_positivi.append(None)
	        casi_testati_ieri = casi_testati_oggi
	    elif (casi_testati_oggi != None):
	        percentuale_test_positivi.append(None)
	        casi_testati_ieri = casi_testati_oggi
	    else:
	        percentuale_test_positivi.append(None)
	        casi_testati_ieri = 0

	    #Aggiornamento variabili
	    deceduti_totali_ieri = deceduti_totali_oggi
	    terapie_intensive_totali_ieri = terapie_intensive_totali_oggi
	    dimessi_guariti_totali_ieri = dimessi_guariti_totali_oggi
	    ricoverati_totali_ieri = ricoverati_totali_oggi
	    isolamento_totali_ieri = isolamento_totali_oggi
	    ospedalizzati_totali_ieri = severi_totali_oggi

giorni = 7

media_date, media_nuovi_deceduti = media_su_giorni(date, nuovi_deceduti, giorni)
_, media_nuove_ti = media_su_giorni(date, nuove_terapie_intensive, giorni)
_, media_variazione_positivi = media_su_giorni(date, variazione_totale_positivi, giorni)
_, media_nuovi_dimessi_guariti = media_su_giorni(date, nuovi_dimessi_guariti, giorni)
_, media_nuovi_ricoverati = media_su_giorni(date, nuovi_ricoverati, giorni)
_, media_nuovi_isolamento = media_su_giorni(date, nuovi_isolamento, giorni)
_, media_nuovi_ospedalizzati = media_su_giorni(date, nuovi_ospedalizzati, giorni)

plt.figure(1)
linea_nuovi_deceduti, = plt.plot(media_date, media_nuovi_deceduti)
linea_nuove_ti, = plt.plot(media_date, media_nuove_ti)
linea_variazione_positivi, = plt.plot(media_date, media_variazione_positivi)
linea_nuovi_dimessi_guariti, = plt.plot(media_date, media_nuovi_dimessi_guariti)
linea_nuovi_ricoverati, = plt.plot(media_date, media_nuovi_ricoverati)
linea_nuovi_isolamento, = plt.plot(media_date, media_nuovi_isolamento)
linea_nuovi_ospedalizzati, = plt.plot(media_date, media_nuovi_ospedalizzati)
linea_nuovi_deceduti.set_label('Nuove morti')
linea_nuove_ti.set_label('Nuove terapie intensive')
linea_variazione_positivi.set_label('Variazione positivi')
linea_nuovi_dimessi_guariti.set_label('Nuovi dimessi/guariti')
linea_nuovi_ricoverati.set_label('Nuovi ricoverati')
linea_nuovi_isolamento.set_label('Nuovi isolamento domiciliare')
linea_nuovi_ospedalizzati.set_label('Nuovi ospedalizzati')
plt.xticks(np.arange(0, len(date), step=4))
plt.xlabel('Date')
plt.ylabel('Numero di persone')
plt.title('Media su ' + str(giorni) + ' giorni di vari dati')
plt.legend()

plt.figure(2)
linea_percentuale_positive, = plt.plot(date, percentuale_test_positivi)
plt.xticks(np.arange(0, len(date), step=4))
plt.ylabel('Percentuale')
plt.xlabel('Date')
plt.title('Percentuale infetti su casi testati')

_, media_deceduti = media_su_giorni(date, deceduti, giorni)
_, media_ti = media_su_giorni(date, terapie_intensive, giorni)
_, media_dimessi_guariti = media_su_giorni(date, dimessi_guariti, giorni)
_, media_ricoverati = media_su_giorni(date, ricoverati_con_sintomi, giorni)
_, media_isolamento = media_su_giorni(date, isolamento_domiciliare, giorni)
_, media_positivi = media_su_giorni(date, totale_positivi, giorni)
_, media_ospedalizzati = media_su_giorni(date, totale_ospedalizzati, giorni)

plt.figure(3)
linea_deceduti, = plt.plot(media_date, media_deceduti)
linea_ti, = plt.plot(media_date, media_ti)
linea_dimessi_guariti, = plt.plot(media_date, media_dimessi_guariti)
linea_ricoverati, = plt.plot(media_date, media_ricoverati)
linea_isolamento, = plt.plot(media_date, media_isolamento)
linea_positivi, = plt.plot(media_date, media_positivi)
linea_ospedalizzati, = plt.plot(media_date, media_ospedalizzati)

linea_deceduti.set_label('Morti totali')
linea_ti.set_label('Terapie intensive attuali')
linea_dimessi_guariti.set_label('Dimessi/guariti totali')
linea_ricoverati.set_label('Ricoverati attuali')
linea_isolamento.set_label('Isolamento domiciliare attuali')
linea_positivi.set_label('Attualmente positivi')
linea_ospedalizzati.set_label('Attualmente ospedalizzati')
plt.xticks(np.arange(0, len(date), step=4))
plt.ylabel('Numero di persone')
plt.xlabel('Date')
plt.title('Media su ' + str(giorni) + ' giorni di vari dati')
plt.legend()

plt.show()