import matplotlib.pyplot as plt
import numpy as np
import csv


COLNAMES = ['nb_nodes', 'inf_times', 'inf_nb_visits', 'supr_times', 'supr_nb_visits', 'med_times', 'med_nb_visits']
AGGREGATE = 1
MARKER_SIZE = 10
MARKER_EVERY = 10
MARKER_WIDTH = 1.5


def get_column(index, filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        column = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                column.append(row[index])
                line_count += 1
        return column


def _chunks(l, n):
    for i in xrange(1, len(l), n):
        yield l[i:i + n]


def _aggregate(value, aggregate):
    if aggregate < 2:
        return value
    returned_value = []
    for chunk in list(_chunks(value, aggregate)):
        returned_value.append(np.mean(np.array(chunk).astype(np.int)))
    returned_value.insert(0, 0)
    return returned_value


# Generation of a complete lattice of 2186 licenses
def generate_exp2():
    plt.subplot(1, 1, 1)
    med = get_column(6, 'expermiental_results/lattice-rand-144-nb_visited-x1-agg50.csv')
    plt.plot(_aggregate(med, AGGREGATE), linewidth=2, color='red')
    plt.xlabel('Number of nodes in the graph')
    plt.ylabel('Number of visited nodes')
    plt.axis([0, len(med), 0, len(med)])
    plt.grid()
    plt.tight_layout()
    plt.savefig('expermiental_results/exp2.png')


# 144 licenses -> Linear order -> ASC, DESC and RANDOM
def generate_exp1():
    plt.subplot(3, 1, 1)
    inf = get_column(2, 'expermiental_results/linear_order-asc-144-nb_visited-x1-agg1.csv')
    sup = get_column(4, 'expermiental_results/linear_order-asc-144-nb_visited-x1-agg1.csv')
    med = get_column(6, 'expermiental_results/linear_order-asc-144-nb_visited-x1-agg1.csv')
    plt.plot(inf, linewidth=2, label="Infimum", marker='+', markersize=MARKER_SIZE+5, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.plot(sup, linewidth=2, label="Supremum", marker='x', markersize=MARKER_SIZE, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.plot(med, linewidth=2, label="Median", marker='.', markersize=MARKER_SIZE-4, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.axis([0, len(inf), 0, len(inf)])
    plt.grid()
    plt.legend(bbox_to_anchor=(1.138, 0.9))
    plt.subplot(3, 1, 2)
    inf2 = get_column(2, 'expermiental_results/linear_order-desc-144-nb_visited-x1-agg1.csv')
    sup2 = get_column(4, 'expermiental_results/linear_order-desc-144-nb_visited-x1-agg1.csv')
    med2 = get_column(6, 'expermiental_results/linear_order-desc-144-nb_visited-x1-agg1.csv')
    plt.plot(inf2, linewidth=2, label="Infimum", marker='+', markersize=MARKER_SIZE+5, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.plot(sup2, linewidth=2, label="Supremum", marker='x', markersize=MARKER_SIZE, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.plot(med2, linewidth=2, label="Median", marker='.', markersize=MARKER_SIZE-4, markevery=MARKER_EVERY, markeredgewidth=MARKER_WIDTH)
    plt.ylabel('Number of visited nodes')
    plt.axis([0, len(inf2), 0, len(inf2)])
    plt.grid()
    plt.subplot(3, 1, 3)
    inf3 = get_column(2, 'expermiental_results/linear_order-rand-144-nb_visited-x5-agg1.csv')
    sup3 = get_column(4, 'expermiental_results/linear_order-rand-144-nb_visited-x5-agg1.csv')
    med3 = get_column(6, 'expermiental_results/linear_order-rand-144-nb_visited-x5-agg1.csv')
    plt.plot(inf3, linewidth=2, label="Infimum")
    plt.plot(sup3, linewidth=2, label="Supremum")
    plt.plot(med3, linewidth=2, label="Median")
    plt.xlabel('Number of nodes in the graph')
    plt.axis([0, len(inf3), 0, len(inf3)])
    plt.grid()
    plt.savefig('expermiental_results/exp1.png')


# Order a set of n licenses taken from the lattice of 2186 licenses
# Average of number of comparison on 3 execution
def generate_exp3():
    plt.figure(figsize=(8.0, 4.0), dpi=900)
    x = get_column(0, 'expermiental_results/quadratic_exec0.csv')
    y1 = get_column(1, 'expermiental_results/quadratic_exec0.csv')
    y2 = get_column(1, 'expermiental_results/quadratic_exec1.csv')
    y3 = get_column(1, 'expermiental_results/quadratic_exec2.csv')
    y_quad = []
    x = map(int, x)
    for xi in map(int, x):
        y_quad.append((xi*xi)/2)
    y = np.mean(np.array([map(int, y1), map(int, y2), map(int, y3)]), axis=0)
    plt.plot(x, y, linewidth=2, color='blue', label='Insertion sort algorithm')
    plt.plot(x, y_quad, 'r--', linewidth=2, color='red', label="Upper bound: $n^{2}/2$")
    plt.ylabel('Average number of comparisons')
    plt.xlabel('Size of graphes')
    plt.grid()
    plt.xlim(100, 2100)
    plt.legend(bbox_to_anchor=(0.75, 1.06))
    plt.tight_layout()
    plt.savefig('expermiental_results/exp3.png')
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig('expermiental_results/exp3_log.png')


# Order a set of n licenses taken from the lattice of 2186 licenses
# Average time to generate the lattice on 3 execution
def generate_exp4():
    plt.figure(figsize=(8.0, 4.0), dpi=900)
    x = get_column(0, 'expermiental_results/quadratic_exec0.csv')
    y1_time = get_column(2, 'expermiental_results/quadratic_exec0.csv')
    y2_time = get_column(2, 'expermiental_results/quadratic_exec1.csv')
    y3_time = get_column(2, 'expermiental_results/quadratic_exec2.csv')
    x = map(int, x)
    y_time = np.mean(np.array([map(float, y1_time), map(float, y2_time), map(float, y3_time)]), axis=0)
    plt.plot(x, y_time, linewidth=2, color='blue', label='Insertion sort algorithm')
    plt.ylabel('Average time to order (s)')
    plt.xlabel('Size of graphes')
    plt.grid()
    plt.tight_layout()
    plt.xlim(100, 2100)
    plt.savefig('expermiental_results/exp4.png')


# generate_exp1()
# generate_exp2()
generate_exp3()
generate_exp4()
