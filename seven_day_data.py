import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import math
import os
import enum
import sys

# Popolazione italiana a Gennaio 2020
TOT_POP_IT = 60244639.0

# Indici mappati ai relativi mesi
MONTHS = {
    1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile", 
    5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto", 
    9: "Settembre", 10: "Ottobre", 11: "Novembre", 
    12: "Dicembre"
};

INFO_REGIONI = {
    "abruzzo": {
        "nome_dato": "Abruzzo",
        "pop": 1305770.0,
        "area": "ABR"
    },
    "basilicata": {
        "nome_dato": "Basilicata",
        "pop": 556934.0,
        "area": "BAS"
    },
    "calabria": {
        "nome_dato": "Calabria",
        "pop": 1924701.0,
        "area": "CAL"
    },
    "campania": {
        "nome_dato": "Campania",
        "pop": 5785861.0,
        "area": "CAM"
    },
    "emilia-romagna": {
        "nome_dato": "Emilia-Romagna",
        "pop": 4467118.0,
        "area": "EMR"
    },
    "friuli venezia giulia": {
        "nome_dato": "Friuli Venezia Giulia",
        "pop": 1211357.0,
        "area": "FVG"
    },
    "lazio": {
        "nome_dato": "Lazio",
        "pop": 5865544.0,
        "area": "LAZ"
    },
    "liguria": {
        "nome_dato": "Liguria",
        "pop": 1543127.0,
        "area": "LIG"
    },
    "lombardia": {
        "nome_dato": "Lombardia",
        "pop": 10103969.0,
        "area": "LOM"
    },
    "marche": {
        "nome_dato": "Marche",
        "pop": 1518400.0,
        "area": "MAR"
    },
    "molise": {
        "nome_dato": "Molise",
        "pop": 302265.0,
        "area": "MOL"
    },
    "p.a. bolzano": {
        "nome_dato": "P.A. Bolzano",
        "pop": 5234.0,
        "area": "PAB"
    },
    "p.a. trento": {
        "nome_dato": "P.A. Trento",
        "pop": 542739.0,
        "area": "PAT"
    },
    "piemonte": {
        "nome_dato": "Piemonte",
        "pop": 4341375.0,
        "area": "PIE"
    },
    "puglia": {
        "nome_dato": "Puglia",
        "pop": 4008296.0,
        "area": "PUG"
    },
    "sardegna": {
        "nome_dato": "Sardegna",
        "pop": 1630474.0,
        "area": "SAR"
    },
    "sicilia": {
        "nome_dato": "Sicilia",
        "pop": 4968410.0,
        "area": "SIC"
    },
    "toscana": {
        "nome_dato": "Toscana",
        "pop": 3722729.0,
        "area": "TOS"
    },
    "umbria": {
        "nome_dato": "Umbria",
        "pop": 880285.0,
        "area": "UMB"
    },
    "valle d'aosta": {
        "nome_dato": "Valle d'Aosta",
        "pop": 125501.0,
        "area": "VDA"
    },
    "veneto": {
        "nome_dato": "Veneto",
        "pop": 4907704.0,
        "area": "VEN"
    }
}

# Directory di questo file
__location__ = os.path.realpath(os.path.join(os.getcwd(),
    os.path.dirname(__file__)))


# @desc     Caricamento dell'andamento nazionale del COVID19 dalla repository
#           GitHub della Protezione Civile
# @param    N/A
# @return   Lista di dizionari contenenti i dati nazionali giornalieri
def caric_dati_it():
    json_file = open(os.path.join(__location__,
        'COVID-DATI/dati-json/dpc-covid19-ita-andamento-nazionale.json'))
    data = json.load(json_file)
    return data


# @desc     Caricamento dell'andamento regionale del COVID19 dalla repository
#           GitHub della Protezione Civile
# @return   Lista di dizionari contenenti i dati nazionali giornalieri
def caric_dati_reg():
    json_file = open('COVID-DATI/dati-json/dpc-covid19-ita-regioni.json')
    data = json.load(json_file)
    return data


# @desc     Caricamento dei dati di una regione italiana dalla repository 
#           opendata
# @return   Lista di dizionari contenenti i dati regionali sui vaccini
def caric_dati_vaccini(area = 'IT'):
    json_file = open('COVID-VACCINI/dati/somministrazioni-vaccini-latest.json')
    dati = json.load(json_file)

    dati_parsati = {}

    for dato in dati['data']:
        if ((area == 'IT') or (dato['area'] == area)):
            data = dato['data_somministrazione'][:10]
            if data in dati_parsati:
                dati_parsati[data]['sesso_femminile'] += dato['sesso_femminile']
                dati_parsati[data]['sesso_maschile'] += dato['sesso_maschile']
                dati_parsati[data]['operatori_sanitari'] += \
                    dato['categoria_operatori_sanitari_sociosanitari']
                dati_parsati[data]['personale_non_sanitario'] += \
                    dato['categoria_personale_non_sanitario']
                dati_parsati[data]['altro'] += dato['categoria_altro']
                dati_parsati[data]['ospiti_rsa'] += dato['categoria_ospiti_rsa']
                dati_parsati[data]['over80'] += dato['categoria_over80']
                dati_parsati[data]['forze_armate'] += dato['categoria_forze_armate']
                dati_parsati[data]['personale_scolastico'] += \
                    dato['categoria_personale_scolastico']
                dati_parsati[data]['prima_dose'] += dato['prima_dose']
                dati_parsati[data]['seconda_dose'] += dato['seconda_dose']
            else:
                nuovo_dato = {
                    'sesso_femminile': dato['sesso_femminile'],
                    'sesso_maschile': dato['sesso_maschile'],
                    'operatori_sanitari':
                        dato['categoria_operatori_sanitari_sociosanitari'],
                    'personale_non_sanitario':
                        dato['categoria_personale_non_sanitario'],
                    'altro': dato['categoria_altro'],
                    'ospiti_rsa': dato['categoria_ospiti_rsa'],
                    'over80': dato['categoria_over80'],
                    'forze_armate': dato['categoria_forze_armate'],
                    'personale_scolastico':
                        dato['categoria_personale_scolastico'],
                    'sesso_femminile': dato['sesso_femminile'],
                    'prima_dose': dato['prima_dose'],
                    'seconda_dose': dato['seconda_dose']
                }
                dati_parsati[data] = nuovo_dato

    return dati_parsati


# @desc     lettura e potenziale calcolo di dati nazionali riguardanti nuovi 
#           positivi, nuovi casi testati, nuovi tamponi effettuati, 
#           ingressi in terapia intensiva e nuovi decessi
# @param    list dati dati nazionali giornalieri caricati
# @return   list dizionari contenenti i dati nazionali giornalieri
def lett_dati_it(dati, dati_vaccini):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []

    # Variabili per calcolare i nuovi casi testati, i nuovi tamponi ed i nuovi
    # morti
    tot_c_ieri = 0
    tot_t_ieri = 0
    tot_m_ieri = 0
    tot_prima_dose = 0
    tot_sec_dose = 0
    ultima_data = ''
    somm_oggi = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati, i nuovi tamponi effettuati e le
    # somministrazioni totali di prima e di seconda dose non
    # sono forniti. Vanno quindi calcolati
    for dato in dati:
        tot_c_oggi = dato['casi_testati']
        tot_t_oggi = dato['tamponi']
        tot_m_oggi = dato['deceduti']
        data = dato['data'][:10]

        # Si prendono i dati da quando inizia ad essere fornito il
        # dato sui casi testati (fine Aprile)
        if (tot_c_oggi != None) and (data != ultima_data) :
            # Calcolo dei nuovi casi testati e dei tamponi
            # effettuati
            nuovi_c = tot_c_oggi - tot_c_ieri
            nuovi_t = tot_t_oggi - tot_t_ieri
            nuovi_m = tot_m_oggi - tot_m_ieri

            if data in dati_vaccini:
                prima_dose_oggi = dati_vaccini[data]['prima_dose']
                sec_dose_oggi = dati_vaccini[data]['seconda_dose']

                tot_prima_dose = tot_prima_dose + prima_dose_oggi
                tot_sec_dose = tot_sec_dose + sec_dose_oggi
                somm_oggi = prima_dose_oggi + sec_dose_oggi

            # Dizionario con i dati che ci interessano
            n_dato = {
                'data': data,
                'nuovi_positivi': dato['nuovi_positivi'],
                'somministrazioni_oggi': somm_oggi,
                'tot_prima_dose': tot_prima_dose,
                'tot_sec_dose': tot_sec_dose
            }

            # Soluzione al problema dei dati che cumulativi che diminuiscono
            if nuovi_c > -1:
                n_dato['nuovi_casi_testati'] = nuovi_c

            if nuovi_t > -1:
                n_dato['nuovi_tamponi'] = nuovi_t

            if (('ingressi_terapia_intensiva' in dato) and 
                (dato['ingressi_terapia_intensiva'] != None)):
                n_dato['entrate_ti'] = dato['ingressi_terapia_intensiva']

            if nuovi_m > -1:
                n_dato['nuovi_morti'] = nuovi_m

            dati_calcolati.append(n_dato)

            # Aggiornamento valori
            tot_c_ieri = tot_c_oggi
            tot_t_ieri = tot_t_oggi
            tot_m_ieri = tot_m_oggi
            ultima_data = data

    return dati_calcolati


# @desc     lettura e potenziale calcolo di dati di una regione riguardanti 
#           nuovi positivi, nuovi casi testati, nuovi tamponi effettuati, 
#           ingressi in terapia intensiva e nuovi decessi
# @param    list dati dati nazionali giornalieri caricati
# @param    string regione la regione i cui dati ritornare
# @return   list dizionari contenenti i dati nazionali giornalieri
def lett_dati_reg(dati, dati_vaccini, regione):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []

    # Variabili per calcolare i nuovi casi testati, i nuovi tamponi ed i nuovi
    # morti
    tot_c_ieri = 0
    tot_t_ieri = 0
    tot_m_ieri = 0
    tot_prima_dose = 0
    tot_sec_dose = 0
    somm_oggi = 0
    ultima_data = ''

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in dati:

        data = dato['data'][:10]
        # Controllo che il dato si riferisca alla regione di nostro
        # interessa
        if (dato['denominazione_regione'] == regione) and (data != ultima_data):
            tot_c_oggi = dato['casi_testati']
            tot_t_oggi = dato['tamponi']
            tot_m_oggi = dato['deceduti']

            # Si prendono i dati da quando inizia ad essere fornito il
            # dato sui casi testati (fine Aprile)
            if tot_c_oggi != None :
                # Calcolo dei nuovi casi testati e dei tamponi
                # effettuati
                nuovi_c = tot_c_oggi - tot_c_ieri
                nuovi_t = tot_t_oggi - tot_t_ieri
                nuovi_m = tot_m_oggi - tot_m_ieri

                if data in dati_vaccini:
                    prima_dose_oggi = dati_vaccini[data]['prima_dose']
                    sec_dose_oggi = dati_vaccini[data]['seconda_dose']

                    tot_prima_dose = tot_prima_dose + prima_dose_oggi
                    tot_sec_dose = tot_sec_dose + sec_dose_oggi
                    somm_oggi = prima_dose_oggi + sec_dose_oggi

                # Dizionario con i dati che ci interessano
                n_dato = {
                    'data': data,
                    'nuovi_positivi': dato['nuovi_positivi'],
                    'somministrazioni_oggi': somm_oggi,
                    'tot_prima_dose': tot_prima_dose,
                    'tot_sec_dose': tot_sec_dose
                }

                # Soluzione al problema dei dati che cumulativi che diminuiscono
                if nuovi_c > -1:
                    n_dato['nuovi_casi_testati'] = nuovi_c

                if nuovi_t > -1:
                    n_dato['nuovi_tamponi'] = nuovi_t

                if (('ingressi_terapia_intensiva' in dato) and 
                    (dato['ingressi_terapia_intensiva'] != None)):
                    n_dato['entrate_ti'] = dato['ingressi_terapia_intensiva']

                if nuovi_m > -1:
                    n_dato['nuovi_morti'] = nuovi_m

                dati_calcolati.append(n_dato)

                # Aggiornamento valori
                tot_c_ieri = tot_c_oggi
                tot_t_ieri = tot_t_oggi
                tot_m_ieri = tot_m_oggi
                ultima_data = data

    return dati_calcolati


# @desc     calcolo di nuovi positivi, nuovi casi testati, nuovi tamponi 
#           effettuati, percentuale di positivi per casi testati, percentuale di
#           positivi per tamponi effettuati ed ingressi in terapia intensiva
#           cumulativi sugli ultimi gg giorni per rel_pop persone
# @param    list dati dati nazionali giornalieri caricati e calcolati
# @param    float tot_pop popolazione totale della nazione/regione da calcolare
# @param    int gg giorni cumulativi dei dati
# @param    float rel_pop popolazione relativa sulla quale calcolare i dati
# @return   list dizionari contenenti i dati nazionali giornalieri calcolati
def calcoli(dati, tot_pop, gg, rel_pop):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []
    
    # Variabili usate per il calcolo dei valori cumulativi sugli 
    # ultimi 7 gg
    tot_nuovi_p = 0
    tot_nuovi_c = 0
    tot_nuovi_t = 0
    tot_entrate_ti = 0
    tot_nuovi_m = 0
    tot_somm_ultimi_7gg = 0
    somm_ultimi_7gg = 0

    # Calcolo del primo valore per ciascuno dei dati
    for i in range(0, 7):
        dati_i = dati[i]
        tot_nuovi_p += dati_i['nuovi_positivi']
        if 'nuovi_casi_testati' in dati_i:
            tot_nuovi_c += dati_i['nuovi_casi_testati']
        if 'nuovi_tamponi' in dati_i:
            tot_nuovi_t += dati_i['nuovi_tamponi']
        if 'entrate_ti' in dati_i:
            tot_entrate_ti += dati_i['entrate_ti']
        if 'nuovi_morti' in dati_i:
            tot_nuovi_m += dati_i['nuovi_morti']
        if 'somministrazioni_oggi' in dati_i:
            somm_ultimi_7gg += dati_i['somministrazioni_oggi']

    # Calcolo e aggiornamento della lista dati_calcolati
    for i in range(7, len(dati)):
        # Calcolo dei nuovi valori
        n_pos_7gg = tot_nuovi_p * rel_pop / tot_pop
        case_7_days_today = tot_nuovi_c * rel_pop / tot_pop
        test_7_days_today = tot_nuovi_t * rel_pop / tot_pop
        n_pos_per_c_today = tot_nuovi_p * 100.0 / tot_nuovi_c
        n_pos_per_t_today = tot_nuovi_p * 100.0 / tot_nuovi_t
        entry_ic_today = tot_entrate_ti * rel_pop / tot_pop
        n_morti_7gg = tot_nuovi_m * rel_pop / tot_pop
        media_mobile_somm = somm_ultimi_7gg / 7

        # Dizionario con i dati che ci interessano
        dato_calcolato = {
            'data': dati[i - 1]['data'],
            'nuovi_pos_7gg': n_pos_7gg,
            'nuovi_casi_test_7gg': case_7_days_today,
            'nuovi_tamponi_7gg': test_7_days_today,
            'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
            'nuovi_pos_per_test_7gg': n_pos_per_t_today,
            'nuove_entrate_ti_7gg': entry_ic_today,
            'nuovi_morti_7gg': n_morti_7gg,
            'media_somm_7gg': media_mobile_somm
        }

        dati_calcolati.append(dato_calcolato)

        dati_oggi = dati[i]
        dati_sett_fa = dati[i - 7]
        # Aggiornamento di tutti i valori
        tot_nuovi_p += dati_oggi['nuovi_positivi'] \
            - dati_sett_fa['nuovi_positivi']
        
        if 'nuovi_casi_testati' in dati_oggi:
            tot_nuovi_c += dati_oggi['nuovi_casi_testati']
        if 'nuovi_casi_testati' in dati_sett_fa:
            tot_nuovi_c -= dati_sett_fa['nuovi_casi_testati']
        
        if 'nuovi_tamponi' in dati_oggi:
            tot_nuovi_t += dati_oggi['nuovi_tamponi']
        if 'nuovi_tamponi' in dati_sett_fa:
            tot_nuovi_t -= dati_sett_fa['nuovi_tamponi']
        
        if 'entrate_ti' in dati_oggi:
            tot_entrate_ti += dati_oggi['entrate_ti']
        if 'entrate_ti' in dati_sett_fa:
            tot_entrate_ti -= dati_sett_fa['entrate_ti']
        
        if 'nuovi_morti' in dati_oggi:
            tot_nuovi_m += dati_oggi['nuovi_morti']
        if 'nuovi_morti' in dati_sett_fa:
            tot_nuovi_m -= dati_sett_fa['nuovi_morti']

        if 'somministrazioni_oggi' in dati_oggi:
            somm_ultimi_7gg += dati_oggi['somministrazioni_oggi']
        if 'somministrazioni_oggi' in dati_sett_fa:
            somm_ultimi_7gg -= dati_sett_fa['somministrazioni_oggi']
    
    # Calcolo dell'ultimo valore
    n_pos_7gg = tot_nuovi_p * rel_pop / tot_pop
    case_7_days_today = tot_nuovi_c * rel_pop / tot_pop
    test_7_days_today = tot_nuovi_t * rel_pop / tot_pop
    n_pos_per_c_today = tot_nuovi_p * 100.0 / tot_nuovi_c
    n_pos_per_t_today = tot_nuovi_p * 100.0 / tot_nuovi_t
    entry_ic_today = tot_entrate_ti * rel_pop / tot_pop
    n_morti_7gg = tot_nuovi_m * rel_pop / tot_pop
    media_mobile_somm = somm_ultimi_7gg / 7

    # Dizionario con i dati che ci interessano
    dato_calcolato = {
        'data': dati[len(dati) - 1]['data'],
        'nuovi_pos_7gg': n_pos_7gg,
        'nuovi_casi_test_7gg': case_7_days_today,
        'nuovi_tamponi_7gg': test_7_days_today,
        'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
        'nuovi_pos_per_test_7gg': n_pos_per_t_today,
        'nuove_entrate_ti_7gg': entry_ic_today,
        'nuovi_morti_7gg': n_morti_7gg,
        'media_somm_7gg': media_mobile_somm
    }

    dati_calcolati.append(dato_calcolato)

    return dati_calcolati


# @desc     stampa la stringa iniziale, seguita dalla data e dal valore
# @param    string data data del dato
# @param    float val il dato
# @param    string str_iniz stringa iniziale da stampare
# @param    bool se_percentuale indica se il valore da stampare è una 
#                               percentuale oppure no
# @return   N/A
# TODO: Cambiare funzione in italiano e commentare
def stampa_valore(data, val, str_iniz, se_percentuale):
    # Recupera giorno e mese in formato stringa di numero
    giorno = data[8] + data[9]
    mese_str_di_num = data[5] + data[6]

    # Conversione del mese da stringa di un numero in un numero
    mese_int = int(mese_str_di_num)

    # Conversione da intero a stringa
    if mese_int not in MONTHS:
        print("Mese non è valido: %d" % mese_int)
        return
    mese_str = MONTHS[mese_int]

    # Formulazione della stringa da stampare
    str_da_stamp = str_iniz + " " + giorno + " " + mese_str + ": " \
                            + f'{round(val, 2):,}'

    # Aggiunta del carattere percentuale
    if se_percentuale:
        str_da_stamp += '%'

    print(str_da_stamp)


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def avg_over_some_days(date, valori, giorni):
    cumulo_valori = 0.0
    media_valori = []
    giorni_float = float(giorni)
    for i in range(giorni):
        cumulo_valori = cumulo_valori + float(valori[i])
    media_valori.append(cumulo_valori / giorni_float)
    for i in range(giorni, len(date)):
        cumulo_valori = cumulo_valori \
            + float(valori[i] - valori[i - giorni])
        media_valori.append(cumulo_valori / giorni_float)
    return date[giorni - 1:], media_valori


def traccia_andamento_vaccini(date, prima_dose, seconda_dose, regione, id):
    plt.figure(id + 6)
    linea_prima_dose, = plt.plot(date, prima_dose)
    linea_prima_dose.set_label('Prima dose')

    linea_seconda_dose, = plt.plot(date, seconda_dose)
    linea_seconda_dose.set_label('Seconda dose')

    plt.xticks(np.arange(0, len(date), step=4))
    plt.xlabel('Date')
    plt.ylabel('Percentuale di popolazione')
    plt.title('Somministrazioni cumulative in %s' % regione)
    plt.legend()


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def traccia_ultimi_giorni(days, dates, n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c, n_pos_per_t, n_ti_7d, n_mor_7gg, media_somm, id, regione):
    start_date = len(dates) - days

    plt.figure(id)
    linea_nuovi_pos, = plt.plot(dates[start_date:], n_pos_7d[start_date:])
    linea_nuovi_pos.set_label('Nuovi positivi')
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)
    plt.legend()

    plt.figure(id + 1)
    linea_test, = plt.plot(dates[start_date:], new_c_7d[start_date:])
    linea_test.set_label('Nuovi casi testati')
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)

    linea_tamponi, = plt.plot(dates[start_date:], new_t_7d[start_date:])
    linea_tamponi.set_label('Nuovi tamponi')
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)
    plt.legend()

    plt.figure(id + 2)
    linea_pos_per_test, = plt.plot(dates[start_date:], n_pos_per_c[start_date:])
    linea_pos_per_test.set_label('Positivi per casi testati in %')
    linea_pos_per_tamponi, = plt.plot(dates[start_date:], n_pos_per_t[start_date:])
    linea_pos_per_tamponi.set_label('Positivi per tamponi in %')
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)
    plt.legend()

    plt.figure(id + 3)
    linea_entrate_ti_7d, = plt.plot(dates[start_date:], n_ti_7d[start_date:])
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.ylabel('Entrate in terapia intensiva')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)

    plt.figure(id + 4)
    linea_nuovi_mor, = plt.plot(dates[start_date:], n_mor_7gg[start_date:])
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.ylabel('Nuovi morti')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
         ' persone' % regione)

    plt.figure(id + 5)
    linea_nuovi_mor, = plt.plot(dates[start_date:], media_somm[start_date:])
    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.ylabel('Migliaia di somministrazioni')
    plt.title('Valori %s media mobile ultimi 7 giorni' % regione)


# @desc     Stampa due valori con rispettive date per paragonarli
# @param    string f_iniz stringa iniziale stampata per identificare i dati
# @param    string d1 data del primo valore
# @param    float v1 primo valore
# @param    string f1 frase iniziale da stampare per il primo valore
# @param    string d2 data del secondo valore
# @param    string v2 il secondo valore
# @param    string f2 frase iniziale da stampare per il secondo valore
# @param    bool se_percentuale indica se il valore è una percentuale oppure no
# @return   N/A
def stampa_due_valori(f_iniz, d1, v1, f1, d2, v2, f2, se_percentuale):
    print(f_iniz)
    stampa_valore(d1, v1, f1, se_percentuale)
    stampa_valore(d2, v2, f2, se_percentuale)


# Calcola i dati interessanti, stampa i dati interessanti di oggi e di
# una settimana fa e poi traccia un grafico dei dati negli ultimi 30 giorni
# @desc     Calcola alcuni dati cumulativi sugli ultimi gg_cum giorni per una 
#           popolazione di pop_rel persone
# @param    list dati TODO
# @param    string regionName TODO
# @param    float tot_pop TODO
# @param    int id_grafico TODO
# @param    int pop_rel popolazione relativa sui quali calcolare i valori
# @param    int gg_cum giorni cumulativi sui quali calcolare i valori
# @param    int gg_trac ultimi giorni di dati da tracciare sul grafico
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def calcoli_e_stampe(dati, regionName, tot_pop, id_grafico, pop_rel = 100000.0, gg_cum = 7, gg_trac = 30):
    # Prima stampa per distinguere Italia e regioni
    print("------------------%s------------------" % regionName)
    print('\nDATI (Nota: I seguenti valori sono cumulativi sugli ultimi %d giorni e ' 
        'sono per ' f'{int(pop_rel):,} persone)\n' % gg_cum)
    dati_calcolati = calcoli(dati, tot_pop, gg_cum, pop_rel)

    # Indici di oggi e di una settimana fa'
    indice_oggi = len(dati_calcolati) - 1
    indice_sett_fa = len(dati_calcolati) - 8

    # Data di oggi e data di una settimana fa'
    data_oggi = dati_calcolati[indice_oggi]['data']
    data_sett_fa = dati_calcolati[indice_sett_fa]['data']

    # New positives in last 7 days
    n_pos_7d_today = dati_calcolati[indice_oggi]['nuovi_pos_7gg']
    # A week ago's new positives in last 7 days
    n_pos_7d_week_ago = dati_calcolati[indice_sett_fa]['nuovi_pos_7gg']
    
    frase_iniziale = "Nuovi positivi:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_7d_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_7d_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's % positive over cases in last 7 days
    n_pos_per_c_today = dati_calcolati[indice_oggi]['nuovi_pos_per_casi_7gg']
        # A week ago's % positive over cases in last 7 days
    n_pos_per_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_casi_7gg']

    frase_iniziale = "\nNuovi positivi per nuovi casi testati:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_per_c_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_per_c_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    # Today's % positive over cases in last 7 days
    n_pos_per_t_today = dati_calcolati[indice_oggi]['nuovi_pos_per_test_7gg']
    # A week ago's % positive over cases in last 7 days
    n_pos_per_t_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_test_7gg']

    frase_iniziale = "\nNuovi positivi per nuovi tamponi:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_per_t_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_per_t_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    # Today's cases per population of 100k over last 7 days
    n_c_today = dati_calcolati[indice_oggi]['nuovi_casi_test_7gg']
    # Week ago's cases per population of 100k over last 7 days
    n_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_casi_test_7gg']

    frase_iniziale = "\nNuovi casi testati:"
    stampa_due_valori(frase_iniziale, data_oggi, n_c_today, 
        "   \u2022 OGGI", data_sett_fa, n_c_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's tests per population over last 7 days
    n_t_today = dati_calcolati[indice_oggi]['nuovi_tamponi_7gg']
    # Week ago's tests per population over last 7 days
    n_t_week_ago = dati_calcolati[indice_sett_fa]['nuovi_tamponi_7gg']

    frase_iniziale = "\nNuovi tamponi:"
    stampa_due_valori(frase_iniziale, data_oggi, n_t_today, 
        "   \u2022 OGGI", data_sett_fa, n_t_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's entries in intensive care per population over last 7 days
    n_ti_today = dati_calcolati[indice_oggi]['nuove_entrate_ti_7gg']
    # Week ago's entries in intensive care per population over last 7 days
    n_ti_week_ago = dati_calcolati[indice_sett_fa]['nuove_entrate_ti_7gg']

    frase_iniziale = "\nIngressi in terapia intensiva:"
    stampa_due_valori(frase_iniziale, data_oggi, n_ti_today, 
        "   \u2022 OGGI", data_sett_fa, n_ti_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's new deaths per population over last 7 days
    n_m_oggi = dati_calcolati[indice_oggi]['nuovi_morti_7gg']
    # Week ago's new deaths per population over last 7 days
    n_m_sett_fa = dati_calcolati[indice_sett_fa]['nuovi_morti_7gg']

    frase_iniziale = "\nNuovi morti:"
    stampa_due_valori(frase_iniziale, data_oggi, n_m_oggi, 
        "   \u2022 OGGI", data_sett_fa, n_m_sett_fa, 
        "   \u2022 SETTIMANA FA", False)

    print("\nVACCINI")

    somm_media_oggi = dati_calcolati[indice_oggi]['media_somm_7gg']
    somm_media_sett_fa = dati_calcolati[indice_sett_fa]['media_somm_7gg']

    frase_iniziale = "\nMedia mobile 7gg nuove somministrazioni:"
    stampa_due_valori(frase_iniziale, data_oggi, somm_media_oggi, 
        "   \u2022 OGGI", data_sett_fa, somm_media_sett_fa, 
        "   \u2022 SETTIMANA FA", False)


    indice_oggi = len(dati) - 1
    indice_sett_fa = len(dati) - 8

    # Today's percentage of people vaccinated with first dose
    n_p_v_oggi = dati[indice_oggi]['tot_prima_dose'] * 100 / tot_pop
    # Week ago's percentage of people vaccinated with first dose
    n_p_v_sett_fa = dati[indice_sett_fa]['tot_prima_dose'] * 100 / tot_pop

    frase_iniziale = "\nTotale vaccinati prima dose:"
    stampa_due_valori(frase_iniziale, data_oggi, n_p_v_oggi, 
        "   \u2022 OGGI", data_sett_fa, n_p_v_sett_fa, 
        "   \u2022 SETTIMANA FA", True)

    # Today's percentage of people vaccinated with second dose
    n_s_v_oggi = dati[indice_oggi]['tot_sec_dose'] * 100 / tot_pop
    # Week ago's percentage of people vaccinated with second dose
    n_s_v_sett_fa = dati[indice_sett_fa]['tot_sec_dose'] * 100 / tot_pop

    frase_iniziale = "\nTotale vaccinati seconda dose:"
    stampa_due_valori(frase_iniziale, data_oggi, n_s_v_oggi, 
        "   \u2022 OGGI", data_sett_fa, n_s_v_sett_fa, 
        "   \u2022 SETTIMANA FA", True)

    print("")

    date = []
    n_pos_7d = []
    new_c_7d = []
    new_t_7d = []
    n_pos_per_c = []
    n_pos_per_t = []
    n_ti_7d = []
    n_m_7gg = []
    media_mobile_somm = []
    
    for i in range(0, len(dati_calcolati)):
        dati_i = dati_calcolati[i]
        date.append(dati_i['data'][5:])
        n_pos_7d.append(dati_i['nuovi_pos_7gg'])
        new_c_7d.append(dati_i['nuovi_casi_test_7gg'])
        new_t_7d.append(dati_i['nuovi_tamponi_7gg'])
        n_pos_per_c.append(dati_i['nuovi_pos_per_casi_7gg'])
        n_pos_per_t.append(dati_i['nuovi_pos_per_test_7gg'])
        n_ti_7d.append(dati_i['nuove_entrate_ti_7gg'])
        n_m_7gg.append(dati_i['nuovi_morti_7gg'])
        media_mobile_somm.append(dati_i['media_somm_7gg'] / 1000.0)
    
    traccia_ultimi_giorni(gg_trac, date, n_pos_7d, new_c_7d, new_t_7d, \
        n_pos_per_c, n_pos_per_t, n_ti_7d, n_m_7gg, media_mobile_somm, id_grafico, regionName)

    # Creare liste da JSON per plottare grafici
    date = []
    prima_dose = []
    seconda_dose = []

    for i in range(0, len(dati)):
        if dati[i]['tot_prima_dose'] > 0:
            date.append(dati[i]['data'][5:])
            prima_dose.append(dati[i]['tot_prima_dose'] * 100.0 / tot_pop)
            seconda_dose.append(dati[i]['tot_sec_dose'] * 100.0 / tot_pop)

    traccia_andamento_vaccini(date, prima_dose, seconda_dose, regionName, id_grafico)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Accetta come argomenti Italia e qualsiasi regione')

    else:
        id = 1
        for arg in sys.argv[1:]:
            
            dati_json = []
            arg_lower = arg.lower()
            pop = 0
            
            if arg_lower == 'italia':
                dati = caric_dati_it()
                dati_vaccini = caric_dati_vaccini()
                dati_json = lett_dati_it(dati, dati_vaccini)
                pop = TOT_POP_IT
            elif arg_lower in INFO_REGIONI:
                info_reg_json = INFO_REGIONI[arg_lower]
                reg_nome = info_reg_json['nome_dato']
                pop = info_reg_json['pop']
                area = info_reg_json['area']

                dati = caric_dati_reg()
                dati_vaccini = caric_dati_vaccini(area)
                dati_json = lett_dati_reg(dati, dati_vaccini, reg_nome)
            else:
                print(arg + ' non è una regione')
                exit()

            calcoli_e_stampe(dati_json, arg.upper(), pop, id)
            
            id += 7

        plt.show()

