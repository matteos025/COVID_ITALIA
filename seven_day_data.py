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
MONTHS = {1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile", 
          5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto", 
          9: "Settembre", 10: "Ottobre", 11: "Novembre", 
          12: "Dicembre"};

POP_REGIONI = {"Abruzzo": 1305770.0, "Basilicata": 556934.0, 
               "Calabria": 1924701.0, "Campania": 5785861.0, 
               "Emilia-Romagna": 4467118.0, "Friuli Venezia Giulia": 1211357.0,
               "Lazio": 5865544.0, "Liguria": 1543127.0,
               "Lombardia": 10103969.0, "Marche": 1518400.0, "Molise": 302265.0,
               "P.A. Bolzano": 5234.0, "P.A. Trento": 542739.0,
               "Piemonte": 4341375.0, "Puglia": 4008296.0,
               "Sardegna": 1630474.0, "Sicilia": 4968410.0,
               "Toscana": 3722729.0, "Umbria": 880285.0,
               "Valle d'Aosta": 125501.0, "Veneto": 4907704.0}

REG_LOW_JSON = {"abruzzo": "Abruzzo", "basilicata": "Basilicata", 
                "calabria": "Calabria", "campania": "Campania", 
                "emilia-romagna": "Emilia-Romagna", 
                "friuli venezia giulia": "Friuli Venezia Giulia", 
                "lazio": "Lazio", "liguria": "Liguria", 
                "lombardia": "Lombardia", "marche": "Marche", 
                "molise": "Molise",
                "p.a. bolzano": "P.A. Bolzano", "p.a. trento": "P.A. Trento",
                "piemonte": "Piemonte", "puglia": "Puglia", 
                "sardegna": "Sardegna", "sicilia": "Sicilia",
                "toscana": "Toscana", "umbria": "Umbria",
                "valle d'aosta": "Valle d'Aosta", "veneto": "Veneto"}

# Directory di questo file
__location__ = os.path.realpath(os.path.join(os.getcwd(), \
                                os.path.dirname(__file__)))


# @desc     caricamento dei dati nazionali dalla repository della Protezione 
#           Civile
# @param    N/A
# @return   lista di dizionari contenenti i dati nazionali giornalieri
def caric_dati_it():
    json_file = open(os.path.join(__location__,
        'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'))
    data = json.load(json_file)
    return data


# @desc     caricamento dei dati di tutte le regioni italiane dalla repository 
#           della Protezione Civile
# @return   lista di dizionari contenenti i dati nazionali giornalieri
def caric_dati_reg():
    json_file = open('COVID-19/dati-json/dpc-covid19-ita-regioni.json')
    data = json.load(json_file)
    return data


# @desc     lettura e potenziale calcolo di dati nazionali riguardanti nuovi 
#           positivi, nuovi casi testati, nuovi tamponi effettuati, 
#           ingressi in terapia intensiva e nuovi decessi
# @param    list dati dati nazionali giornalieri caricati
# @return   list dizionari contenenti i dati nazionali giornalieri
def lett_dati_it(dati):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []

    # Variabili per calcolare i nuovi casi testati, i nuovi tamponi ed i nuovi
    # morti
    tot_c_ieri = 0
    tot_t_ieri = 0
    tot_m_ieri = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in dati:
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
            
            # Dato fornito a partire dal 4 Dicembre
            entrate_ti = 0
            if (('ingressi_terapia_intensiva' in dato) and 
                    (dato['ingressi_terapia_intensiva'] != None)):
                entrate_ti = dato['ingressi_terapia_intensiva']

            # Dizionario con i dati che ci interessano
            dato = {
                'data': dato['data'][5:10],
                'nuovi_positivi': dato['nuovi_positivi'],
                'nuovi_casi_testati': nuovi_c,
                'nuovi_tamponi': nuovi_t,
                'entrate_ti': entrate_ti,
                'nuovi_morti': nuovi_m
            }

            dati_calcolati.append(dato)

            # Aggiornamento valori
            tot_c_ieri = tot_c_oggi
            tot_t_ieri = tot_t_oggi
            tot_m_ieri = tot_m_oggi

    return dati_calcolati


# @desc     lettura e potenziale calcolo di dati di una regione riguardanti 
#           nuovi positivi, nuovi casi testati, nuovi tamponi effettuati, 
#           ingressi in terapia intensiva e nuovi decessi
# @param    list dati dati nazionali giornalieri caricati
# @param    string regione la regione i cui dati ritornare
# @return   list dizionari contenenti i dati nazionali giornalieri
def lett_dati_reg(dati, regione):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []

    # Variabili per calcolare i nuovi casi testati, i nuovi tamponi ed i nuovi
    # morti
    tot_c_ieri = 0
    tot_t_ieri = 0
    tot_m_ieri = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in dati:
        # Controllo che il dato si riferisca alla regione di nostro
        # interessa
        if dato['denominazione_regione'] == regione:
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
                
                # Dato fornito a partire dal 4 Dicembre
                entrate_ti = 0
                if (('ingressi_terapia_intensiva' in dato) and 
                        (dato['ingressi_terapia_intensiva'] != None)):
                    entrate_ti = dato['ingressi_terapia_intensiva']

                # Dizionario con i dati che ci interessano
                dato = {
                    'data' : dato['data'][5:10],
                    'nuovi_positivi' : dato['nuovi_positivi'],
                    'nuovi_casi_testati' : nuovi_c,
                    'nuovi_tamponi' : nuovi_t,
                    'entrate_ti' : entrate_ti,
                    'nuovi_morti': nuovi_m
                }

                dati_calcolati.append(dato)

                # Aggiornamento valori
                tot_c_ieri = tot_c_oggi
                tot_t_ieri = tot_t_oggi
                tot_m_ieri = tot_m_oggi

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

    # Calcolo del primo valore per ciascuno dei dati
    for i in range(0, 7):
        dati_i = dati[i]
        tot_nuovi_p += dati_i['nuovi_positivi']
        tot_nuovi_c += dati_i['nuovi_casi_testati']
        tot_nuovi_t += dati_i['nuovi_tamponi']
        tot_entrate_ti += dati_i['entrate_ti']
        tot_nuovi_m += dati_i['nuovi_morti']

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

        # Dizionario con i dati che ci interessano
        dato_calcolato = {
            'data': dati[i - 1]['data'],
            'nuovi_pos_7gg': n_pos_7gg,
            'nuovi_casi_test_7gg': case_7_days_today,
            'nuovi_tamponi_7gg': test_7_days_today,
            'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
            'nuovi_pos_per_test_7gg': n_pos_per_t_today,
            'nuove_entrate_ti_7gg': entry_ic_today,
            'nuovi_morti_7gg': n_morti_7gg
        }

        dati_calcolati.append(dato_calcolato)

        dati_oggi = dati[i]
        dati_sett_fa = dati[i - 7]
        # Aggiornamento di tutti i valori
        tot_nuovi_p += dati_oggi['nuovi_positivi'] \
            - dati_sett_fa['nuovi_positivi']
        tot_nuovi_c += dati_oggi['nuovi_casi_testati'] \
            - dati_sett_fa['nuovi_casi_testati']
        tot_nuovi_t += dati_oggi['nuovi_tamponi'] \
            - dati_sett_fa['nuovi_tamponi']
        tot_entrate_ti += dati_oggi['entrate_ti'] - dati_sett_fa['entrate_ti']
        tot_nuovi_m += dati_oggi['nuovi_morti'] - dati_sett_fa['nuovi_morti']
    
    # Calcolo dell'ultimo valore
    n_pos_7gg = tot_nuovi_p * rel_pop / tot_pop
    case_7_days_today = tot_nuovi_c * rel_pop / tot_pop
    test_7_days_today = tot_nuovi_t * rel_pop / tot_pop
    n_pos_per_c_today = tot_nuovi_p * 100.0 / tot_nuovi_c
    n_pos_per_t_today = tot_nuovi_p * 100.0 / tot_nuovi_t
    entry_ic_today = tot_entrate_ti * rel_pop / tot_pop
    n_morti_7gg = tot_nuovi_m * rel_pop / tot_pop

    # Dizionario con i dati che ci interessano
    dato_calcolato = {
        'data': dati[len(dati) - 1]['data'],
        'nuovi_pos_7gg': n_pos_7gg,
        'nuovi_casi_test_7gg': case_7_days_today,
        'nuovi_tamponi_7gg': test_7_days_today,
        'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
        'nuovi_pos_per_test_7gg': n_pos_per_t_today,
        'nuove_entrate_ti_7gg': entry_ic_today,
        'nuovi_morti_7gg': n_morti_7gg
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
    giorno = data[3] + data[4]
    mese_str_di_num = data[0] + data[1]

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


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def print_expected_20(num_day_avg, avg_n_pos, avg_diff):
    last_avg_n_pos_diff = avg_diff[len(avg_diff) - 1]
    last_avg_n_pos = avg_n_pos[len(avg_n_pos) - 1]
    shift = math.floor(num_day_avg / 2)
    giorni_per_20 = round(((20.0 - last_avg_n_pos) \
        / last_avg_n_pos_diff) - shift)
    if giorni_per_20 >= 0:
        data_20 = datetime.now() + timedelta(days=giorni_per_20)
        print("Giorno arrivo a 20.00 previsto: " + str(data_20)[:10])
    else:
        print("Trend negativo, previsione a 20.0 impossibile")


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def traccia_ultimi_giorni(days, dates, n_pos_7d, new_c_7d, new_t_7d, \
                          n_pos_per_c, n_pos_per_t, n_ti_7d, n_mor_7gg, id, 
                          regione):
    start_date = len(dates) - days

    plt.figure(id)

    linea_nuovi_pos, = plt.plot(dates[start_date:], n_pos_7d[start_date:])
    linea_nuovi_pos.set_label('Nuovi positivi')

    linea_test, = plt.plot(dates[start_date:], new_c_7d[start_date:])
    linea_test.set_label('Nuovi casi testati * 10')

    linea_tamponi, = plt.plot(dates[start_date:], new_t_7d[start_date:])
    linea_tamponi.set_label('Nuovi tamponi * 10')

    linea_pos_per_test, = plt.plot(dates[start_date:], n_pos_per_c[start_date:])
    linea_pos_per_test.set_label('Positivi per casi testati in millesimi di %')

    linea_pos_per_tamponi, = plt.plot(dates[start_date:], \
       n_pos_per_t[start_date:])
    linea_pos_per_tamponi.set_label('Positivi per tamponi in millesimi di %')

    linea_entrate_ti_7d, = plt.plot(dates[start_date:], n_ti_7d[start_date:])
    linea_entrate_ti_7d.set_label('Entrate in terapia intensiva / 100')

    linea_nuovi_mor, = plt.plot(dates[start_date:], n_mor_7gg[start_date:])
    linea_nuovi_mor.set_label('Nuovi morti / 10')

    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
        ' persone' % regione)
    plt.legend()


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def find_last_decrease(dates, n_pos_7d):
    date = "00/00"
    val_prima = 0.0
    val = 0.0

    for i in range(7, len(dates)):
        if n_pos_7d[i] < n_pos_7d[i - 7]:
            date_prima = dates[i - 7]
            date = dates[i]
            val_prima = n_pos_7d[i - 7]
            val =n_pos_7d[i]

    print(date_prima + ": %.2f" % val_prima)
    print(date + ": %.2f" % val)


# @desc     TODO
# @param    TODO
# @param    TODO
# @param    TODO
# @return   TODO
# TODO: Cambiare funzione in italiano e commentare
def find_last_above(dates, n_pos_7d, num_above):
    date = "00/00"
    val = 0.0

    for i in range(7, len(dates)):
        if n_pos_7d[i] > num_above:
            date = dates[i]
            val = n_pos_7d[i]

    print(("Last above %d: " % num_above) + date + " - %.2f" % val)


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
def calcoli_e_stampe(dati, regionName, tot_pop, id_grafico, pop_rel = 100000.0,
                     gg_cum = 7, gg_trac = 30):
    # Prima stampa per distinguere Italia e regioni
    print("------------------%s------------------" % regionName)
    print('\nNota: I seguenti valori sono per ' f'{int(pop_rel):,}' 
          ' persone\n')
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
    
    frase_iniziale = "Nuovi positivi ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_7d_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_7d_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's % positive over cases in last 7 days
    n_pos_per_c_today = dati_calcolati[indice_oggi]['nuovi_pos_per_casi_7gg']
        # A week ago's % positive over cases in last 7 days
    n_pos_per_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_casi_7gg']

    frase_iniziale = "\nPositivi per casi testati ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_per_c_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_per_c_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    # Today's % positive over cases in last 7 days
    n_pos_per_t_today = dati_calcolati[indice_oggi]['nuovi_pos_per_test_7gg']
    # A week ago's % positive over cases in last 7 days
    n_pos_per_t_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_test_7gg']

    frase_iniziale = "\nPositivi per tamponi ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_pos_per_t_today, 
        "   \u2022 OGGI", data_sett_fa, n_pos_per_t_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    # Today's cases per population of 100k over last 7 days
    n_c_today = dati_calcolati[indice_oggi]['nuovi_casi_test_7gg']
    # Week ago's cases per population of 100k over last 7 days
    n_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_casi_test_7gg']

    frase_iniziale = "\nCasi testati ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_c_today, 
        "   \u2022 OGGI", data_sett_fa, n_c_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's tests per population over last 7 days
    n_t_today = dati_calcolati[indice_oggi]['nuovi_tamponi_7gg']
    # Week ago's tests per population over last 7 days
    n_t_week_ago = dati_calcolati[indice_sett_fa]['nuovi_tamponi_7gg']

    frase_iniziale = "\nTamponi ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_t_today, 
        "   \u2022 OGGI", data_sett_fa, n_t_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's entries in intensive care per population over last 7 days
    n_ti_today = dati_calcolati[indice_oggi]['nuove_entrate_ti_7gg']
    # Week ago's entries in intensive care per population over last 7 days
    n_ti_week_ago = dati_calcolati[indice_sett_fa]['nuove_entrate_ti_7gg']

    frase_iniziale = "\nIngressi in terapia intensiva ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_ti_today, 
        "   \u2022 OGGI", data_sett_fa, n_ti_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Today's new deaths per population over last 7 days
    n_m_oggi = dati_calcolati[indice_oggi]['nuovi_morti_7gg']
    # Week ago's new deaths per population over last 7 days
    n_m_sett_fa = dati_calcolati[indice_sett_fa]['nuovi_morti_7gg']

    frase_iniziale = "\nNuovi morti ultimi 7 giorni:"
    stampa_due_valori(frase_iniziale, data_oggi, n_m_oggi, 
        "   \u2022 OGGI", data_sett_fa, n_m_sett_fa, 
        "   \u2022 SETTIMANA FA", False)

    print("")

    # Creare liste da JSON per plottare grafici
    date = []
    n_pos_7d = []
    new_c_7d = []
    new_t_7d = []
    n_pos_per_c = []
    n_pos_per_t = []
    n_ti_7d = []
    n_m_7gg = []
    
    for i in range(0, len(dati_calcolati)):
        dati_i = dati_calcolati[i]
        date.append(dati_i['data'])
        n_pos_7d.append(dati_i['nuovi_pos_7gg'])
        new_c_7d.append(dati_i['nuovi_casi_test_7gg'] / 10.0)
        new_t_7d.append(dati_i['nuovi_tamponi_7gg'] / 10.0)
        n_pos_per_c.append(dati_i['nuovi_pos_per_casi_7gg'] * 10.0)
        n_pos_per_t.append(dati_i['nuovi_pos_per_test_7gg'] * 10.0)
        n_ti_7d.append(dati_i['nuove_entrate_ti_7gg'] * 100.0)
        n_m_7gg.append(dati_i['nuovi_morti_7gg'] * 10.0)
    
    traccia_ultimi_giorni(gg_trac, date, n_pos_7d, new_c_7d, new_t_7d, \
        n_pos_per_c, n_pos_per_t, n_ti_7d, n_m_7gg, id_grafico, regionName)


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
                dati_json = lett_dati_it(dati)
                pop = TOT_POP_IT
            else:
                arg_json = REG_LOW_JSON[arg_lower]
                if arg_json in POP_REGIONI:
                    dati = caric_dati_reg()
                    dati_json = lett_dati_reg(dati, arg_json)
                    pop = POP_REGIONI[arg_json]
                else:
                    print(arg + ' non è una regione')
                    exit()

            calcoli_e_stampe(dati_json, arg.upper(), pop, id)
            
            id += 1

        plt.show()

