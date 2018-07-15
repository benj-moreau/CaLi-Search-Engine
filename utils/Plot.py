import plotly.offline as py
import plotly.graph_objs as go


def draw(time_array1, time_array2):
    trace_infimum = go.Scatter(
        x=range(len(time_array1)),
        y=time_array1,
        name='Infimum'
    )
    trace_supremum = go.Scatter(
        x=range(len(time_array2)),
        y=time_array2,
        name='Supremum'
    )
    data = [trace_infimum, trace_supremum]
    layout = dict(title='Average time to add a license in the graph',
                  xaxis=dict(title='Graph size'),
                  yaxis=dict(title='Execution time (ms)')
                  )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='basic-line', auto_open=True)
