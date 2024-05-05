from flask import Flask, request, jsonify
from Item import Item
from Printer import Printer
import random
from geopy.distance import great_circle
import time
import random
from deap import base, creator, tools, algorithms
import numpy as np


app = Flask(__name__)





items = [
    Item ("1.1", [3], 1440*5,3, -7.797957910935617, 110.41786149494659), #STTA
    Item ("1.2", [3], 1440*5,2,-7.797957910935617, 110.41786149494659), #STTA
    Item ("1.3", [2], 572*2,3, -7.797957910935617, 110.41786149494659), #STTA
    Item ("1.4", [2], 300*2,1,-7.797957910935617, 110.41786149494659), #STTA
    Item ("2.1", [2], 691*5,1,-7.77194178661424, 110.30647808145225), #SMA N godean
    Item ("2.2", [3], 691*2,2,-7.77194178661424, 110.30647808145225), #SMA N godean
    Item ("3.1", [2], 873*5,0, -7.742084599022894, 110.43241716888542), #Budimulia 1
    Item ("3.2", [3], 873*2,2, -7.742084599022894, 110.43241716888542), #Budimulia 1
    Item ("4.1", [1], 154*5,2, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("4.2", [2], 305*5,0, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("4.3", [3], 719*2,0, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("4.4", [1], 154*2,2, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("4.5", [2], 305*2,1, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("4.6", [3], 719*2,1, -7.739099938941269, 110.4001860526165), #Halpoint
    Item ("5.1", [3], 906*5,0, -7.831553788099929, 110.31778656611162), #rumah
    Item ("5.2", [1], 149*5,0, -7.831553788099929, 110.31778656611162), #rumah
    Item ("5.3", [3], 906*2,2, -7.831553788099929, 110.31778656611162), #rumah
    Item ("5.4", [1], 149*2,0, -7.831553788099929, 110.31778656611162), #rumah
    Item ("5.5", [1],	371*5,1, -7.831553788099929, 110.31778656611162),#rumah
    Item ("6.1", [3], 991*5,0, -7.984251325284412, 110.3054995397715), #SD Unggulan Muhammadiyah paris
    Item ("6.2", [3], 991*2,1, -7.984251325284412, 110.3054995397715), #SD Unggulan Muhammadiyah paris
    Item ("7.1", [1], 174*5,1, -7.799523471003249, 110.3525658084406), #SMA Teladan
    Item ("7.2", [3],	991*5,1, -7.799523471003249, 110.3525658084406), #SMA Teladan
    Item ("8.1", [1], 187*5,2, -7.743622703318905, 110.35026443727529), #RSA UGM
    Item ("8.2", [1], 391*5,1, -7.743580179322621, 110.3503073526166),#RSA UGM
    Item ("8.3", [2],	572*5,1, -7.743580179322621, 110.3503073526166),#RSA UGM
    Item ("8.4", [2],	300*5,2, -7.743580179322621, 110.3503073526166),#RSA UGM
    Item ("9.1", [2], 391*5,0, -7.661698596532625, 110.42158268329821), #GRhasia
    Item ("10.1", [3], 1440*5,0, -7.753790087393336, 110.40076478969902), #JIH
    Item ("11.1", [3], 1440*5,0, -7.768371793708117, 110.37349565261695), #RSUP sarjito
    Item ("12.1", [3], 1240*5,2, -7.886037551894553, 110.38799390930478), #RS Nurhidayah (imogiri timur)
    Item ("12.2", [2],	305*5,2, -7.886037551894553, 110.38799390930478), #RS Nurhidayah (imogiri timur)
    Item ("12.3", [3],	906*5,2,-7.886037551894553, 110.38799390930478), #RS Nurhidayah (imogiri timur)
    Item ("13.1", [1], 134*5,2, -7.776197549105719, 110.37373866795832), #MAN 1 Yogyakarta
    Item ("14.1", [1], 150*5,1, -7.854846459747203, 110.15848079494718), #SMA 1 Wates
    Item ("14.2", [3],	691*5,2,-7.854846459747203, 110.15848079494718), #SMA 1 Wates
    Item ("15.2", [3],	873*5,2, -7.485307132181383, 110.21809437960172),#RSUD Magelang
    Item ("15.3", [1],	154*5,2, -7.485307132181383, 110.21809437960172),#RSUD Magelang
    Item ("15.1", [2], 603*5,1, -7.485307132181383, 110.21809437960172),#RSUD Magelang
    Item ("16.1", [1],	203*5,1, -7.818211542199179, 110.34931018241201),#SMAN 1 kasihan
]

printers = [
    Printer("1.1",1, -7.765815728148268, 110.37382632452378), #UGM
    Printer("1.2",2, -7.765815728148268, 110.37382632452378), #UGM
    # Printer("1.3",3, -7.765815728148268, 110.37382632452378), #UGM
    Printer("2.1",1, -7.811021918563302, 110.32101165077016), #UMY
    Printer("2.2",2, -7.811021918563302, 110.32101165077016), #UMY
    #Printer("2.3",3, -7.811021918563302, 110.32101165077016), #UMY
    Printer("3.1",1, -7.686262258990693, 110.4105695669599), #UII
    Printer("3.2",1, -7.686262258990693, 110.4105695669599), #UII
    # Printer("3.3",2, -7.686262258990693, 110.4105695669599), #UII
    # Printer("3.4",3, -7.686262258990693, 110.4105695669599), #UII
]




IND_SIZE = len(items)

# Check if there items can't be printed at all
MAX_PRINTERS_DIM = max(printers,key=lambda x:x.a)
valid_items = []
messages=[]
for i in items:
    if i.dim[0] > MAX_PRINTERS_DIM.a:
        messages.append(f"Item {i.name} doesnt have any valid printers, Item DIM: {i.dim[0]}, printers MAX DIM: {MAX_PRINTERS_DIM.a}")
    valid_items.append(i)

items = valid_items

valid_combinations = {i: [p for p in range(len(printers)) if items[i].dim[0] <= printers[p].a]
                    for i in range(len(items))}

# Genetic Algorithm constants:
POPULATION_SIZE = 100
MAX_GENERATIONS = 200

# Set the random seed:
RANDOM_SEED = 10
random.seed(RANDOM_SEED)

# Define a route for handling POST requests
@app.route('/run-simulation', methods=['GET'])
def run_simulation():
    start_time = time.time()
    res = {"Printers":[],"errors":"","status":"","messages":[]}


    toolbox = base.Toolbox()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)
    toolbox = base.Toolbox()
    toolbox.register("individualCreator", generate_individual, creator.Individual)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    distance_cache = {}

    toolbox.register("evaluate", printerValue)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("mate", custom_cx)
    toolbox.register("mutate", custom_mutation, indpb=1.0/len(items))


    population = toolbox.populationCreator(n=POPULATION_SIZE)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)


    # Perform the NSGA-II algorithm:
    population, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=POPULATION_SIZE,
                                                        lambda_=2*POPULATION_SIZE, cxpb=0.6, mutpb=0.2, ngen=MAX_GENERATIONS, stats=stats, verbose=True)
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    #analisis pareto front
    pareto_values = [ind.fitness.values for ind in pareto_front]

    # revisi
    # Menguraikan nilai objektif
    objektif1 = [val[0] for val in pareto_values]
    objektif2 = [val[1] for val in pareto_values]
    objektif3 = [val[2] for val in pareto_values]

    # Plotting data
    # Menetapkan warna berdasarkan salah satu objektif (misalnya objektif3)
    # Plotting data dengan warna

    # Extract statistics:
    maxFitnessValues, meanFitnessValues = logbook.select("min", "avg")



    end_time = time.time()

    print("Waktu Eksekusi: {:.2f} detik".format(end_time - start_time))

    

    cnt_printer = [0]*len(printers)
    for i in range(len(pareto_front[0])):
        cnt_printer[pareto_front[0][i]]+= items[i].value
        printers[pareto_front[0][i]].item_has.append(items[i])
    for i in range(len(printers)):
        print('Printer {} time spent: {} '.format(i,cnt_printer[i]))
        res["Printers"].append(cnt_printer[i])
        printers[i].set_time_spent(cnt_printer[i])
        printers[i].set_timeseries()
    res["messages"]=messages
    return jsonify(res),200




if __name__ == '__main__':
    app.run(debug=True)




def valid_ind(bits):
    return all(bits[i] in valid_combinations[i] for i in range(len(bits)))

# Function to generate a valid individual
def generate_individual(icls):
    bits = []
    for i in range(len(items)):
        if valid_combinations[i]:
            bits.append(random.choice(valid_combinations[i]))
        else:
            raise ValueError(f"No valid printer for item {i} with dim {items[i].dim[0]}")
    return icls(bits)
def custom_mutation(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = random.choice(valid_combinations[i])
    return individual,
def custom_cx(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]

    if not valid_ind(ind1) or not valid_ind(ind2):
        ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2] = ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2]
    return ind1, ind2


def calculate_distance(coord1, coord2, distance_cache):
    key = (coord1, coord2)
    if key not in distance_cache:
        distance_cache[key] = great_circle(coord1, coord2).kilometers
    return distance_cache[key]

def printerValue(individual):
    # Pastikan panjang individual sesuai
    if not (len(individual) == len(items)):
        raise ValueError("Length of 'individual' and 'items' must be the same")

    max_time = 0
    total_lateness = 0
    total_distance = 0

    tasks_per_printer = {p: [] for p in range(len(printers))}
    for item_index, printer_index in enumerate(individual):
        item = items[item_index]
        printer = printers[printer_index]
        distance = calculate_distance((item.latitude, item.longitude), (printer.latitude, printer.longitude), distance_cache)
        total_distance += distance
        tasks_per_printer[printer_index].append((item.due, item.value))

    for printer_index, tasks in tasks_per_printer.items():
        tasks.sort(key=lambda due: due[0])
        current_time = 0
        for due, process_time in tasks:
            current_time += process_time
            max_time = max(max_time, current_time)
            lateness = max(0, current_time - (due + 1) * 1440)
            total_lateness += lateness
            printers[printer_index].set_time_spent(current_time)

    return total_distance, total_lateness, max_time
    for printer_index, tasks in tasks_per_printer.items():
        # Mengurutkan tugas berdasarkan 'due' (prioritas)
        tasks.sort(key=lambda x: x[0])
        current_time = 0
        for due, process_time in tasks:
            current_time += process_time
            #max_time = max(max_time, current_time)
            lateness = max(0, current_time - (due + 1) * 1440)  # Sesuaikan perhitungan lateness jika diperlukan
            total_lateness += lateness
            printers[printer_index].set_time_spent(current_time)

    return total_distance, total_lateness, max_time


