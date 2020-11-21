import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import math
import os

# Italian population end of May
it_pop = 60062012.0

# Lumbardy population end of May
lum_pop = 10067773.0

# Current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Loads data from github repo
def load_data_italy():
    json_file = open(os.path.join(__location__, 
        'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'))
    data = json.load(json_file)
    return data

def load_data_regions():
    json_file = open('COVID-19/dati-json/dpc-covid19-ita-regioni.json')
    data = json.load(json_file)
    return data

# Reads relevant data from loaded data
def read_data_italy(data):
    #Initialize empty lists
    dates = []
    n_pos = []
    new_new_cases = []
    new_new_tests = []
    new_c_yesterday = 0
    new_t_yesterday = 0

    #Add relevant data to lists
    for dato in data:
        new_c_today = dato['casi_testati']
        new_t_today = dato['tamponi']
        if new_c_today != None:
            dates.append(dato['data'][5:10])
            n_pos.append(dato['nuovi_positivi'])
            new_new_cases.append(new_c_today - new_c_yesterday)
            new_new_tests.append(new_t_today - new_t_yesterday)
            new_c_yesterday = new_c_today
            new_t_yesterday = new_t_today

    return dates, n_pos, new_new_cases, new_new_tests

# Reads relevant data from loaded data
def read_data_lumbardy(data):
    #Initialize empty lists
    dates = []
    n_pos = []
    new_new_cases = []
    new_new_tests = []
    new_c_yesterday = 0
    new_t_yesterday = 0

    #Add relevant data to lists
    for dato in data:
        if dato['denominazione_regione'] == 'Lombardia':
            new_c_today = dato['casi_testati']
            new_t_today = dato['tamponi']
            if new_c_today != None:
                dates.append(dato['data'][5:10])
                n_pos.append(dato['nuovi_positivi'])
                new_new_cases.append(new_c_today - new_c_yesterday)
                new_new_tests.append(new_t_today - new_t_yesterday)
                new_c_yesterday = new_c_today
                new_t_yesterday = new_t_today

    return dates, n_pos, new_new_cases, new_new_tests

# Calculates new positives in the last 7 days and diff over each day
def calcs(dates, n_pos, new_c, new_t, population):
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
        total_cases = total_cases + n_pos[i]
        total_new_c = total_new_c + new_c[i]
        total_new_t = total_new_t + new_t[i]

    # Calculate and update lists
    for i in range(7, len(dates)):
        # Calculate new values
        n_pos_7d_today = total_cases * relative_pop / population
        case_7_days_today = total_new_c * 10000 / population
        test_7_days_today = total_new_t * 10000 / population
        n_pos_per_c_today = total_cases * 1000 / total_new_c
        n_pos_per_t_today = total_cases * 1000 / total_new_t

        # Add calculated values to lists
        n_pos_7d.append(n_pos_7d_today)
        new_c_7d.append(case_7_days_today)
        new_t_7d.append(test_7_days_today)
        n_pos_per_c_7_days.append(n_pos_per_c_today)
        n_pos_per_t_7_days.append(n_pos_per_t_today)

        # Update yesterday's new positives
        total_cases = total_cases - n_pos[i - 7] + n_pos[i]
        total_new_c = total_new_c - new_c[i - 7] + new_c[i]
        total_new_t = total_new_t - new_t[i - 7] + new_t[i]
    
    # Calculate last value
    n_pos_7d_today = total_cases * relative_pop / population
    case_7_days_today = total_new_c * 10000 / population
    test_7_days_today = total_new_t * 10000 / population
    n_pos_per_c_today = total_cases * 1000 / total_new_c
    n_pos_per_t_today = total_cases * 1000 / total_new_t

    # Aggiunta a liste
    n_pos_7d.append(n_pos_7d_today)
    new_c_7d.append(case_7_days_today)
    new_t_7d.append(test_7_days_today)
    n_pos_per_c_7_days.append(n_pos_per_c_today)
    n_pos_per_t_7_days.append(n_pos_per_t_today)

    return dates[6:], n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c_7_days, n_pos_per_t_7_days

# Print date and relative new positive value
def print_val(date, n_pos, print_str, is_percent):
    day = date[3] + date[4]
    month = date[0] + date[1]
    str_to_print = print_str + " " + day + "/" + month + ": %.2f" % n_pos
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
        cumulo_valori = cumulo_valori + float(valori[i] - valori[i - giorni])
        media_valori.append(cumulo_valori / giorni_float)
    return date[giorni - 1:], media_valori


def print_expected_20(num_day_avg, avg_n_pos, avg_diff):
    last_avg_n_pos_diff = avg_diff[len(avg_diff) - 1]
    last_avg_n_pos = avg_n_pos[len(avg_n_pos) - 1]
    shift = math.floor(num_day_avg / 2)
    giorni_per_20 = round(((20.0 - last_avg_n_pos) / last_avg_n_pos_diff) - shift)
    if giorni_per_20 >= 0:
        data_20 = datetime.now() + timedelta(days=giorni_per_20)
        print("Giorno arrivo a 20.00 previsto: " + str(data_20)[:10])
    else:
        print("Trend negativo, previsione a 20.0 impossibile")


def plot_last_days(days, dates, n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c, n_pos_per_t, id, regione):
    start_date = len(dates) - days

    plt.figure(id)
    linea_nuovi_pos, = plt.plot(dates[start_date:], n_pos_7d[start_date:])
    linea_test, = plt.plot(dates[start_date:], new_c_7d[start_date:])
    linea_tamponi, = plt.plot(dates[start_date:], new_t_7d[start_date:])
    linea_pos_per_test, = plt.plot(dates[start_date:], n_pos_per_c[start_date:])
    linea_pos_per_tamponi, = plt.plot(dates[start_date:], n_pos_per_t[start_date:])
    linea_nuovi_pos.set_label('Nuovi positivi')
    linea_test.set_label('Nuovi casi testati * 10')
    linea_tamponi.set_label('Nuovi tamponi * 10')
    linea_pos_per_test.set_label('Positivi per casi testati in millesimi di %')
    linea_pos_per_tamponi.set_label('Positivi per tamponi in millesimi di %')

    plt.xticks(np.arange(0, days, step=2))
    plt.xlabel('Date')
    plt.title('Valori %s cumulativi ultimi 7 giorni per 100.000 persone' % regione)
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
    
def calculate_and_print(dates, n_pos, new_c, new_t, pop, isRegion, id, regionName = None):
    if not isRegion:
        print("------------------ITALIA------------------")
    else:
        print("------------------%s------------------" % regionName)

    # Update dates and calculate new positives in last 7 days,
    # daily difference over new positives in last 7 das, 
    # new tests last 7 days, new positives per tests ylast 7 days
    dates, n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c, n_pos_per_t = calcs(dates, n_pos, new_c, new_t, pop)

    # New positives in last 7 days
    n_pos_7d_today = n_pos_7d[len(n_pos_7d) - 1]
    date_today = dates[len(dates) - 1]
    
    # Print out new positives last 7 days
    print_val(date_today, n_pos_7d_today, 
        "Nuovi positivi ultimi 7 giorni OGGI", False)

    # A week ago's new positives in last 7 days
    n_pos_7d_week_ago = n_pos_7d[len(n_pos_7d) - 8]
    date_week_ago = dates[len(dates) - 8]

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_7d_week_ago, 
        "Nuovi positivi ultimi 7 giorni SETTIMANA FA", False)

    # Today's % positive over cases in last 7 days
    n_pos_per_c_today = n_pos_per_c[len(n_pos_per_c) - 1] / 10

    # Print out week ago's new positives in last 7 days
    print_val(date_today, n_pos_per_c_today, 
        "Positivi per casi testati ultimi 7 giorni OGGI", True)

    # A week ago's % positive over cases in last 7 days
    n_pos_per_c_week_ago = n_pos_per_c[len(n_pos_per_c) - 8] / 10

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_per_c_week_ago, 
        "Positivi per casi testati ultimi 7 giorni SETTIMANA FA", True)

    # Today's % positive over cases in last 7 days
    n_pos_per_t_today = n_pos_per_t[len(n_pos_per_t) - 1] / 10

    # Print out week ago's new positives per tests in last 7 days
    print_val(date_today, n_pos_per_t_today, 
        "Positivi per tamponi ultimi 7 giorni OGGI", True)

    # A week ago's % positive over cases in last 7 days
    n_pos_per_t_week_ago = n_pos_per_t[len(n_pos_per_t) - 8] / 10

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_pos_per_t_week_ago, 
        "Positivi per tamponi ultimi 7 giorni SETTIMANA FA", True)

    # Today's cases per population of 100k over last 7 days
    n_c_today = new_c_7d[len(new_c_7d) - 1] * 10

    # Print today's cases per population of 100k over last 7 days
    print_val(date_today, n_c_today, 
        "Casi testati ultimi 7 giorni OGGI", False)

    # Week ago's cases per population of 100k over last 7 days
    n_c_week_ago = new_c_7d[len(new_c_7d) - 8] * 10

    # Print out week ago's cases per population of 100k over last 7 days
    print_val(date_week_ago, n_c_week_ago, 
        "Casi testati ultimi 7 giorni SETTIMANA FA", False)

    # Today's tests per population over last 7 days
    n_t_today = new_t_7d[len(new_t_7d) - 1] * 10

    # Print out week ago's new positives in last 7 days
    print_val(date_today, n_t_today, 
        "Tamponi ultimi 7 giorni OGGI", False)

     # Week ago's tests per population over last 7 days
    n_t_week_ago = new_t_7d[len(new_t_7d) - 8] * 10

    # Print out week ago's new positives in last 7 days
    print_val(date_week_ago, n_t_week_ago, 
        "Tamponi ultimi 7 giorni SETTIMANA FA", False)

    if not isRegion:
        plot_last_days(30, dates, n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c, n_pos_per_t, id, "ITALIA")
    else:
        plot_last_days(30, dates, n_pos_7d, new_c_7d, new_t_7d, n_pos_per_c, n_pos_per_t, id, regionName)


if __name__ == "__main__":

    data_it = load_data_italy()
    data_reg = load_data_regions()

    # Read dates, new positives and new tests
    dates_it, n_pos_it, new_c_it, new_t_it = read_data_italy(data_it)
    dates_lum, n_pos_lum, new_c_lum, new_t_lum = read_data_lumbardy(data_reg)
    
    calculate_and_print(dates_it, n_pos_it, new_c_it, new_t_it, it_pop, False, 1)

    calculate_and_print(dates_lum, n_pos_lum, new_c_lum, new_t_lum, lum_pop, True, 2, "LOMBARDIA")    
    
    plt.show()

