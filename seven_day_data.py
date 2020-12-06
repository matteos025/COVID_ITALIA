import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import math
import os
import enum

# Popolazione italiana a fine Maggio
IT_POP = 60062012.0

# Popolazione lombarda a fine Maggio
LUM_POP = 10067773.0

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
def load_data_italy():
    json_file = open(os.path.join(__location__, 
        'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'))
    data = json.load(json_file)
    return data

# Caricamento dei dati lombardi dalla repository della protezione 
# civile
def load_data_regions():
    json_file = open('COVID-19/dati-json/dpc-covid19-ita-regioni.json')
    data = json.load(json_file)
    return data

# Lettura nazionale di date, nuovi casi testati, nuovi tamponi 
# e nuovi positivi, che vengono poi ritornati in 4 liste
def read_data_italy(data):
    # Liste vuote:
    # dati - dizionari contententi data, nuovi positivi, nuovi casi 
    #        testati e nuovi tamponi
    # date
    # nuovi positivi
    # nuovi casi testati
    # nuovi tamponi
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

        # Il dato sui casi testati inizia ad essere fornito a
        # Marzo/Aprile le liste iniziano da lì
        if tot_c_oggi != None :
            nuovi_casi_testati_oggi = tot_c_oggi - tot_c_ieri
            nuovi_tamponi_oggi = tot_t_oggi - tot_t_ieri

            dato = {
                'data' : dato['data'][5:10],
                'nuovi_positivi' : dato['nuovi_positivi'],
                'nuovi_casi_testati' : nuovi_casi_testati_oggi,
                'nuovi_tamponi' : nuovi_tamponi_oggi
            }

            dati.append(dato)

            # Aggiornamento valori
            tot_c_ieri = tot_c_oggi
            tot_t_ieri = tot_t_oggi

    return dati


# Lettura lombarda di date, nuovi casi testati, nuovi tamponi 
# e nuovi positivi, che vengono poi ritornati in 4 liste
def read_data_lumbardy(data):
    # Liste vuote:
    # dati - dizionari contententi data, nuovi positivi, nuovi casi
    #        testati e nuovi tamponi
    # date
    # nuovi_positivi
    # nuovi_casi_testati
    # nuovi_tamponi
    dati = []

    # Variabili per calcolare i nuovi casi testati e i nuovi tamponi
    tot_c_ieri = 0
    tot_t_ieri = 0

    # Aggiunta dei dati alle liste per ogni data disponibile
    # Nota: I nuovi casi testati ed i nuovi tamponi effettuati non
    # sono forniti, quindi vanno calcolati
    for dato in data:
        if dato['denominazione_regione'] == 'Lombardia':
            tot_c_oggi = dato['casi_testati']
            tot_t_oggi = dato['tamponi']

            # Il dato sui casi testati inizia ad essere fornito a
            # Marzo/Aprile le liste iniziano da lì
            if tot_c_oggi != None :
                nuovi_casi_testati_oggi = tot_c_oggi - tot_c_ieri
                nuovi_tamponi_oggi = tot_t_oggi - tot_t_ieri

                dato = {
                    'data' : dato['data'][5:10],
                    'nuovi_positivi' : dato['nuovi_positivi'],
                    'nuovi_casi_testati' : nuovi_casi_testati_oggi,
                    'nuovi_tamponi' : nuovi_tamponi_oggi
                }

                dati.append(dato)

                # Aggiornamento valori
                tot_c_ieri = tot_c_oggi
                tot_t_ieri = tot_t_oggi

    return dati


# Calcolo dei nuovi positivi negli ultimi 7 giorni e delle 
# differenze tra i giorni
def calcs(dati, population):
    dati_calcolati =[]
    n_pos_7d = []
    n_pos_7d_diff = []
    new_c_7d = []
    new_t_7d = []
    n_pos_per_c_7_days = []
    n_pos_per_t_7_days = []
    total_cases = 0
    total_new_c = 0
    total_new_t = 0
    relative_pop = 100000

    # Calculate first value
    for i in range(0, 7):
        total_cases = total_cases + dati[i]['nuovi_positivi']
        total_new_c = total_new_c + dati[i]['nuovi_casi_testati']
        total_new_t = total_new_t + dati[i]['nuovi_tamponi']

    # Calculate and update lists
    for i in range(7, len(dati)):
        # Calculate new values
        n_pos_7d_today = total_cases * relative_pop / population
        case_7_days_today = total_new_c * relative_pop / population
        test_7_days_today = total_new_t * relative_pop / population
        n_pos_per_c_today = total_cases * 100.0 / total_new_c
        n_pos_per_t_today = total_cases * 100.0 / total_new_t

        # Add calculated values to lists
        n_pos_7d.append(n_pos_7d_today)
        new_c_7d.append(case_7_days_today)
        new_t_7d.append(test_7_days_today)
        n_pos_per_c_7_days.append(n_pos_per_c_today)
        n_pos_per_t_7_days.append(n_pos_per_t_today)

        dato_calcolato = {
            'data': dati[i]['data'],
            'nuovi_pos_7gg': n_pos_7d_today,
            'nuovi_casi_test_7gg': case_7_days_today,
            'nuovi_tamponi_7gg': test_7_days_today,
            'nuovi_pos_per_casi_7gg': n_pos_per_c_today,
            'nuovi_pos_per_test_7gg': n_pos_per_t_today
        }

        dati_calcolati.append(dato_calcolato)

        # Update yesterday's new positives
        total_cases = total_cases - dati[i - 7]['nuovi_positivi'] \
            + dati[i]['nuovi_positivi']
        total_new_c = total_new_c \
            - dati[i - 7]['nuovi_casi_testati'] \
            + dati[i]['nuovi_casi_testati']
        total_new_t = total_new_t - dati[i - 7]['nuovi_tamponi'] \
            + dati[i]['nuovi_tamponi']
    
    # Calculate last value
    n_pos_7d_today = total_cases * relative_pop / population
    case_7_days_today = total_new_c * relative_pop / population
    test_7_days_today = total_new_t * relative_pop / population
    n_pos_per_c_today = total_cases * relative_pop / total_new_c
    n_pos_per_t_today = total_cases * relative_pop / total_new_t

    # Aggiunta a liste
    n_pos_7d.append(n_pos_7d_today)
    new_c_7d.append(case_7_days_today)
    new_t_7d.append(test_7_days_today)
    n_pos_per_c_7_days.append(n_pos_per_c_today)
    n_pos_per_t_7_days.append(n_pos_per_t_today)

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
                   n_pos_per_c, n_pos_per_t, id, regione):
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
    linea_nuovi_pos.set_label('Nuovi positivi')
    linea_test.set_label('Nuovi casi testati * 10')
    linea_tamponi.set_label('Nuovi tamponi * 10')
    linea_pos_per_test.set_label( \
        'Positivi per casi testati in millesimi di %')
    linea_pos_per_tamponi.set_label( \
        'Positivi per tamponi in millesimi di %')

    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000 \
        persone' % regione)
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


def calculate_and_print(dati, pop, isRegion, id, regionName = None):
    if not isRegion:
        print("-------------------ITALIA-------------------")
    else:
        print("------------------%s------------------" % regionName)

    # Update dates and calculate new positives in last 7 days,
    # daily difference over new positives in last 7 das, 
    # new tests last 7 days, new positives per tests ylast 7 days
    dati_calcolati = calcs(dati, pop)
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

    # Creare liste da JSON per plottare grafici
    date = []
    n_pos_7d = []
    new_c_7d = []
    new_t_7d = []
    n_pos_per_c = []
    n_pos_per_t = []
    for dato in dati_calcolati:
        date.append(dato['data'])
        n_pos_7d.append(dato['nuovi_pos_7gg'])
        new_c_7d.append(dato['nuovi_casi_test_7gg'] / 10)
        new_t_7d.append(dato['nuovi_tamponi_7gg'] / 10)
        n_pos_per_c.append(dato['nuovi_pos_per_casi_7gg'] * 10)
        n_pos_per_t.append(dato['nuovi_pos_per_test_7gg'] * 10)

    if not isRegion:
        plot_last_days(30, date, n_pos_7d, new_c_7d, new_t_7d, \
            n_pos_per_c, n_pos_per_t, id, "ITALIA")
    else:
        plot_last_days(30, date, n_pos_7d, new_c_7d, new_t_7d, \
           n_pos_per_c, n_pos_per_t, id, regionName)


if __name__ == "__main__":
    # Caricamento dei dati della protezione civile
    data_it = load_data_italy()
    data_lum = load_data_regions()

    # Read dates, new positives and new tests
    dati_json_it = read_data_italy(data_it)
    dati_json_lum = read_data_lumbardy(data_lum)
    
    calculate_and_print(dati_json_it, IT_POP, False, 1)

    calculate_and_print(dati_json_lum, LUM_POP, True, 2, "LOMBARDIA")    
    
    plt.show()
