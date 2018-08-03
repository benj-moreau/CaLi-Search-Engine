import plotly.offline as py
import plotly.graph_objs as go


def draw(measure_array_inf, measure_array_sup, measure_array_med, structure, order, limit, measure):
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
    py.plot(fig, filename='expermiental_results/{}-{}-{}-{}.html'.format(structure, order, limit, measure), auto_open=False)
