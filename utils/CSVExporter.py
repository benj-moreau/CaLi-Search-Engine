import csv
import itertools


def export(inf_times, inf_nb_visits, supr_times, supr_nb_visits, med_times, med_nb_visits, structure, order, limit, measure, nb_exec, aggregate):
    with open('expermiental_results/{}-{}-{}-{}-x{}-agg{}.csv'.format(structure, order, limit, measure, nb_exec, aggregate), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['nb_nodes', 'inf_times', 'inf_nb_visits', 'supr_times', 'supr_nb_visits', 'med_times', 'med_nb_visits'])
        nb_nodes = range(0, len(inf_times))
        for row in itertools.izip(nb_nodes, inf_times, inf_nb_visits, supr_times, supr_nb_visits, med_times, med_nb_visits):
            writer.writerow(row)
