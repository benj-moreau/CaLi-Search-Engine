import csv


def export(inf_times, inf_nb_visits, supr_times, supr_nb_visits, med_times, med_nb_visits, structure, order, limit, measure, nb_exec, aggregate):
    with open('expermiental_results/{}-{}-{}-{}-x{}-agg{}.csv'.format(structure, order, limit, measure, nb_exec, aggregate), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['nb_nodes'] + range(0, len(inf_times)))
        writer.writerow(['inf_time'] + inf_times)
        writer.writerow(['inf_nb_visits'] + inf_nb_visits)
        writer.writerow(['supr_times'] + supr_times)
        writer.writerow(['supr_nb_visits'] + supr_nb_visits)
        writer.writerow(['med_times'] + med_times)
        writer.writerow(['med_nb_visits'] + med_nb_visits)
