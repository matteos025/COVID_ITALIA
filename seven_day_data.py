import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import math
import os
import enum

# Popolazione italiana a fine Maggio
TOT_POP_IT = 60062012.0

# Popolazione lombarda a fine Maggio
TOT_POP_LOM = 10067773.0

# Indici mappati ai relativi mesi
MONTHS = {1 : "Gennaio", 2 : "Febbraio", 3 : "Marzo", 4 : "Aprile", 
          5 : "Maggio", 6 : "Giugno", 7 : "Luglio", 8 : "Agosto", 
          9 : "Settembre", 10 : "Ottobre", 11 : "Novembre", 
          12 : "Dicembre"};

# Directory di questo file
__location__ = os.path.realpath(os.path.join(os.getcwd(), \
                                os.path.dirname(__file__)))


# Caricamento dei dati nazionali dalla repository della protezione 
# civile
def caric_dati_it():
    json_file = open(os.path.join(__location__, 
        'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'))
    data = json.load(json_file)
    return data


# Caricamento dei dati regionali dalla repository della protezione 
# civile
def caric_dati_reg():
    json_file = open('COVID-19/dati-json/dpc-covid19-ita-regioni.json')
    data = json.load(json_file)
    return data


# Lettura dei dati nazionali caricati in una lista di dizionari. I dati
# raccolti sono:
#   - Date
#   - Nuovi positivi
#   - Nuovi casi testati 
#   - Nuovi tamponi effettuati
#   - Ingressi in terapia intensiva
def lett_dati_it(data):
    # Lista di dizionari, poi ritornata dalla funzione
    dati = []

    # Variabili per calcolare i nuovi casi testati e i nuovi tamponi
    tot_c_ieri = 0
    tot_t_ieri = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in data:
        tot_c_oggi = dato['casi_testati']
        tot_t_oggi = dato['tamponi']

        # Si prendono i dati da quando inizia ad essere fornito il
        # dato sui casi testati (fine Aprile)
        if tot_c_oggi != None :
            # Calcolo dei nuovi casi testati e dei tamponi
            # effettuati
            nuovi_c = tot_c_oggi - tot_c_ieri
            nuovi_t = tot_t_oggi - tot_t_ieri
            
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
                'entrate_ti' : entrate_ti
            }

            dati.append(dato)

            # Aggiornamento valori
            tot_c_ieri = tot_c_oggi
            tot_t_ieri = tot_t_oggi

    return dati


# Lettura dei dati di una regione caricati in una lista di dizionari.
# I dati raccolti sono:
#   - Date
#   - Nuovi positivi
#   - Nuovi casi testati 
#   - Nuovi tamponi effettuati
#   - Ingressi in terapia intensiva
def lett_dati_reg(data, regione):
    # Lista di dizionari, poi ritornata dalla funzione
    dati = []

    # Variabili per calcolare i nuovi casi testati e i nuovi tamponi
    tot_c_ieri = 0
    tot_t_ieri = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in data:

        # Controllo che il dato si riferisca alla regione di nostro
        # interessa
        if dato['denominazione_regione'] == regione:
            tot_c_oggi = dato['casi_testati']
            tot_t_oggi = dato['tamponi']

            # Si prendono i dati da quando inizia ad essere fornito il
            # dato sui casi testati (fine Aprile)
            if tot_c_oggi != None :
                # Calcolo dei nuovi casi testati e dei tamponi
                # effettuati
                nuovi_casi_testati_oggi = tot_c_oggi - tot_c_ieri
                nuovi_tamponi_oggi = tot_t_oggi - tot_t_ieri
                
                # Dato fornito a partire dal 4 Dicembre
                entrate_ti = 0
                if (('ingressi_terapia_intensiva' in dato) and 
                        (dato['ingressi_terapia_intensiva'] != None)):
                    entrate_ti = dato['ingressi_terapia_intensiva']

                # Dizionario con i dati che ci interessano
                dato = {
                    'data' : dato['data'][5:10],
                    'nuovi_positivi' : dato['nuovi_positivi'],
                    'nuovi_casi_testati' : nuovi_casi_testati_oggi,
                    'nuovi_tamponi' : nuovi_tamponi_oggi,
                    'entrate_ti' : entrate_ti
                }

                dati.append(dato)

                # Aggiornamento valori
                tot_c_ieri = tot_c_oggi
                tot_t_ieri = tot_t_oggi

    return dati


# Calcolo dei valori cumulativi sugli ultimi 7 giorni per 100.000 
# persone di:
#   - Nuovi positivi
#   - Nuovi casi testati 
#   - Nuovi tamponi effettuati
#   - Ingressi in terapia intensiva
def calcoli(dati, tot_pop):
    # Lista di dizionari, poi ritornata dalla funzione
    dati_calcolati = []
    
    # Variabili usate per il calcolo dei valori cumulativi sugli 
    # ultimi 7 gg
    tot_nuovi_p = 0
    tot_nuovi_c = 0
    tot_nuovi_t = 0
    tot_entrate_ti = 0
    
    # Popolazione relativa.
    # TODO: Trasformarlo in un parametro che viene passato
    rel_pop = 100000

    # Calcolo del primo valore per ciascuno dei dati
    for i in range(0, 7):
        tot_nuovi_p += dati[i]['nuovi_positivi']
        tot_nuovi_c += dati[i]['nuovi_casi_testati']
        tot_nuovi_t += dati[i]['nuovi_tamponi']
        tot_entrate_ti += dati[i]['entrate_ti']

    # Calcolo e aggiornamento della lista dati_calcolati
    for i in range(7, len(dati)):
        # Calcolo dei nuovi valori
        n_pos_7gg = tot_nuovi_p * rel_pop / tot_pop
        case_7_days_today = tot_nuovi_c * rel_pop / tot_pop
        test_7_days_today = tot_nuovi_t * rel_pop / tot_pop
        n_pos_per_c_today = tot_nuovi_p * 100.0 / tot_nuovi_c
        n_pos_per_t_today = tot_nuovi_p * 100.0 / tot_nuovi_t
        entry_ic_today = tot_entrate_ti * rel_pop / tot_pop

        # Dizionario con i dati che ci interessano
        dato_calcolato = {
            'data': dati[i - 1]['data'],
            'nuovi_pos_7gg': n_pos_7gg,
            'nuovi_casi_test_7gg': case_7_days_today,
            'nuovi_tamponi_7gg': test_7_days_today,
            'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
            'nuovi_pos_per_test_7gg': n_pos_per_t_today,
            'nuove_entrate_ti_7gg' : entry_ic_today
        }

        dati_calcolati.append(dato_calcolato)

        # Aggiornamento di tutti i valori
        tot_nuovi_p += dati[i]['nuovi_positivi'] \
            - dati[i - 7]['nuovi_positivi']
        tot_nuovi_c += dati[i]['nuovi_casi_testati'] \
            - dati[i - 7]['nuovi_casi_testati']
        tot_nuovi_t += dati[i]['nuovi_tamponi'] \
            - dati[i - 7]['nuovi_tamponi']
        tot_entrate_ti += dati[i]['entrate_ti'] \
            - dati[i - 7]['entrate_ti']
    
    # Calcolo dell'ultimo valore
    n_pos_7gg = tot_nuovi_p * rel_pop / tot_pop
    case_7_days_today = tot_nuovi_c * rel_pop / tot_pop
    test_7_days_today = tot_nuovi_t * rel_pop / tot_pop
    n_pos_per_c_today = tot_nuovi_p * 100.0 / tot_nuovi_c
    n_pos_per_t_today = tot_nuovi_p * 100.0 / tot_nuovi_t
    entry_ic_today = tot_entrate_ti * rel_pop / tot_pop

    # Dizionario con i dati che ci interessano
    dato_calcolato = {
        'data': dati[len(dati) - 1]['data'],
        'nuovi_pos_7gg': n_pos_7gg,
        'nuovi_casi_test_7gg': case_7_days_today,
        'nuovi_tamponi_7gg': test_7_days_today,
        'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
        'nuovi_pos_per_test_7gg': n_pos_per_t_today,
        'nuove_entrate_ti_7gg' : entry_ic_today
    }

    dati_calcolati.append(dato_calcolato)

    return dati_calcolati


# Print date and relative new positive value
def print_val(date, n_pos, print_str, is_percent):
    day = date[3] + date[4]
    month_num_str = date[0] + date[1]
    month_num_int = int(month_num_str)
    month_str = MONTHS[month_num_int]
    if month_str == None:
        print("Month is not valid")
        return
    str_to_print = print_str + " " + day + " " + month_str \
                   + ": %.2f" % n_pos
    if is_percent:
        str_to_print = str_to_print + "%"
    print(str_to_print)


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


def plot_last_days(days, dates, n_pos_7d, new_c_7d, new_t_7d, \
                   n_pos_per_c, n_pos_per_t, n_ti_7d, id, regione):
    start_date = len(dates) - days

    plt.figure(id)
    linea_nuovi_pos, = plt.plot(dates[start_date:], \
        n_pos_7d[start_date:])
    linea_test, = plt.plot(dates[start_date:], new_c_7d[start_date:])
    linea_tamponi, = plt.plot(dates[start_date:], \
       new_t_7d[start_date:])
    linea_pos_per_test, = plt.plot(dates[start_date:], \
       n_pos_per_c[start_date:])
    linea_pos_per_tamponi, = plt.plot(dates[start_date:], \
       n_pos_per_t[start_date:])
    linea_entrate_ti_7d, = plt.plot(dates[start_date:], \
       n_ti_7d[start_date:])
    linea_nuovi_pos.set_label('Nuovi positivi')
    linea_test.set_label('Nuovi casi testati * 10')
    linea_tamponi.set_label('Nuovi tamponi * 10')
    linea_pos_per_test.set_label( \
       'Positivi per casi testati in millesimi di %')
    linea_pos_per_tamponi.set_label( \
       'Positivi per tamponi in millesimi di %')
    linea_entrate_ti_7d.set_label('Entrate in terapia intensiva / 100')

    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000'
        ' persone' % regione)
    plt.legend()


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


def find_last_above(dates, n_pos_7d, num_above):
    date = "00/00"
    val = 0.0

    for i in range(7, len(dates)):
        if n_pos_7d[i] > num_above:
            date = dates[i]
            val = n_pos_7d[i]

    print(("Last above %d: " % num_above) + date + " - %.2f" % val)


def calcoli_e_stampe(dati, pop, isRegion, id, regionName = None):
    if not isRegion:
        print("-------------------ITALIA-------------------")
    else:
        print("------------------%s------------------" % regionName)

    dati_calcolati = calcoli(dati, pop)

    # Indici di oggi e di una settimana fa'
    indice_oggi = len(dati_calcolati) - 1
    indice_sett_fa = len(dati_calcolati) - 8

    # New positives in last 7 days
    n_pos_7d_today = \
        dati_calcolati[indice_oggi]['nuovi_pos_7gg']
    date_today = dati_calcolati[indice_oggi]['data']
    
    print("Nuovi positivi ultimi 7 giorni:")

    # Print out new positives last 7 days
    print_val(date_today, n_pos_7d_today,
        "   \u2022 OGGI", False)

    # A week ago's new positives in last 7 days
    n_pos_7d_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_7gg']
    date_week_ago = dati_calcolati[indice_sett_fa]['data']

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_7d_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    print("\nPositivi per casi testati ultimi 7 giorni:")

    # Today's % positive over cases in last 7 days
    n_pos_per_c_today = \
        dati_calcolati[indice_oggi]['nuovi_pos_per_casi_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_today, n_pos_per_c_today, 
        "   \u2022 OGGI", True)

    # A week ago's % positive over cases in last 7 days
    n_pos_per_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_casi_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_per_c_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    print("\nPositivi per tamponi ultimi 7 giorni:")

    # Today's % positive over cases in last 7 days
    n_pos_per_t_today = \
        dati_calcolati[indice_oggi]['nuovi_pos_per_test_7gg']

    # Print out week ago's new positives per tests in last 7 days
    print_val(date_today, n_pos_per_t_today, 
        "   \u2022 OGGI", True)

    # A week ago's % positive over cases in last 7 days
    n_pos_per_t_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_pos_per_test_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_per_t_week_ago, 
        "   \u2022 SETTIMANA FA", True)

    print("\nCasi testati ultimi 7 giorni:")

    # Today's cases per population of 100k over last 7 days
    n_c_today = dati_calcolati[indice_oggi]['nuovi_casi_test_7gg']

    # Print today's cases per population of 100k over last 7 days
    print_val(date_today, n_c_today, 
        "   \u2022 OGGI", False)

    # Week ago's cases per population of 100k over last 7 days
    n_c_week_ago = \
        dati_calcolati[indice_sett_fa]['nuovi_casi_test_7gg']

    # Print out week ago's cases per population of 100k over last 
    # 7 days
    print_val(date_week_ago, n_c_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    print("\nTamponi ultimi 7 giorni:")

    # Today's tests per population over last 7 days
    n_t_today = dati_calcolati[indice_oggi]['nuovi_tamponi_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_today, n_t_today, 
        "   \u2022 OGGI", False)

    # Week ago's tests per population over last 7 days
    n_t_week_ago = dati_calcolati[indice_sett_fa]['nuovi_tamponi_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_t_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    print("\nIngressi in terapia intensiva ultimi 7 giorni:")

    # Today's entries in intensive care per population over last 7 
    # days
    n_ti_today = dati_calcolati[indice_oggi]['nuove_entrate_ti_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_today, n_ti_today, 
        "   \u2022 OGGI", False)

    # Week ago's entries in intensive care per population over last 7
    # days
    n_ti_week_ago = \
        dati_calcolati[indice_sett_fa]['nuove_entrate_ti_7gg']

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_ti_week_ago, 
        "   \u2022 SETTIMANA FA", False)

    # Creare liste da JSON per plottare grafici
    date = []
    n_pos_7d = []
    new_c_7d = []
    new_t_7d = []
    n_pos_per_c = []
    n_pos_per_t = []
    n_ti_7d = []
    for i in range(0, len(dati_calcolati)):
        date.append(dati_calcolati[i]['data'])
        n_pos_7d.append(dati_calcolati[i]['nuovi_pos_7gg'])
        new_c_7d.append(
            dati_calcolati[i]['nuovi_casi_test_7gg'] / 10.0)
        new_t_7d.append(dati_calcolati[i]['nuovi_tamponi_7gg'] / 10.0)
        n_pos_per_c.append(
            dati_calcolati[i]['nuovi_pos_per_casi_7gg'] * 10.0)
        n_pos_per_t.append(
            dati_calcolati[i]['nuovi_pos_per_test_7gg'] * 10.0)
        n_ti_7d.append(
            dati_calcolati[i]['nuove_entrate_ti_7gg'] * 100.0)
    
    if not isRegion:
        plot_last_days(30, date, n_pos_7d, new_c_7d, new_t_7d, \
            n_pos_per_c, n_pos_per_t, n_ti_7d, id, "ITALIA")
    else:
        plot_last_days(30, date, n_pos_7d, new_c_7d, new_t_7d, \
           n_pos_per_c, n_pos_per_t, n_ti_7d, id, regionName)


if __name__ == "__main__":
    dati_it = caric_dati_it()
    dati_reg = caric_dati_reg()

    # TODO: Per calcolare e stampare più regioni bisognerebbe
    # che questa fosse una lista di stringhe di nomi di regione
    reg = 'Lombardia'

    dati_json_it = lett_dati_it(dati_it)
    dati_json_lom = lett_dati_reg(dati_reg, reg)
    
    calcoli_e_stampe(dati_json_it, TOT_POP_IT, False, 1)
    calcoli_e_stampe(dati_json_lom, TOT_POP_LOM, True, 2, reg.upper())
    
    plt.show()
