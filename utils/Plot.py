import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


def draw(data_inf, data_sup, data_med, structure, order, limit, measure, nb_exec):
    measure_array_inf = []
    for key, value in data_inf.iteritems():
        measure_array_inf.append(value)
    measure_array_inf = list(np.average(measure_array_inf, axis=0))
    trace_infimum = go.Scatter(
        x=range(len(measure_array_inf)),
        y=measure_array_inf,
        name='Infimum',
        line=dict(
            color=('rgb(169, 203, 160)'),
            width=2,
            dash='dash'
        )
    )
    measure_array_sup = []
    for key, value in data_sup.iteritems():
        measure_array_sup.append(value)
    measure_array_sup = list(np.average(measure_array_sup, axis=0))
    trace_supremum = go.Scatter(
        x=range(len(measure_array_sup)),
        y=measure_array_sup,
        name='Supremum',
        line=dict(
            color=('rgb(60, 84, 206)'),
            width=2,
            dash='dot'
        )
    )
    measure_array_med = []
    for key, value in data_med.iteritems():
        measure_array_med.append(value)
    measure_array_med = list(np.average(measure_array_med, axis=0))
    trace_median = go.Scatter(
        x=range(len(measure_array_med)),
        y=measure_array_med,
        name='Median',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=3
        )
    )
    data = [trace_infimum, trace_supremum, trace_median]
    if measure == 'time':
        y_title = 'Execution time (ms)'
    else:
        y_title = 'Number of visited nodes'
    layout = dict(
                  xaxis=dict(title='Number of nodes'),
                  yaxis=dict(title=y_title)
                  )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='expermiental_results/{}-{}-{}-{}-x{}.html'.format(structure, order, limit, measure, nb_exec), auto_open=False)
