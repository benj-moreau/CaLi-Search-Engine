import plotly.offline as py
import plotly.graph_objs as go


def draw(measure_array_inf, measure_array_sup, measure_array_med, structure, order, limit, measure):
    trace_infimum = go.Scatter(
        x=range(len(measure_array_inf)),
        y=measure_array_inf,
        name='Infimum'
    )
    trace_supremum = go.Scatter(
        x=range(len(measure_array_sup)),
        y=measure_array_sup,
        name='Supremum'
    )
    trace_median = go.Scatter(
        x=range(len(measure_array_med)),
        y=measure_array_med,
        name='Median'
    )
    data = [trace_infimum, trace_supremum, trace_median]
    if measure == 'time':
        plot_title = 'Average time to add a license in the graph'
        y_title = 'Execution time (ms)'
    else:
        plot_title = 'Number of comparisons to add a license in the graph'
        y_title = 'Number of comparisons (nodes)'
    layout = dict(title=plot_title,
                  xaxis=dict(title='Graph size (nodes)'),
                  yaxis=dict(title=y_title)
                  )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='expermiental_results/{}-{}-{}-{}.html'.format(structure, order, limit, measure), auto_open=False)
