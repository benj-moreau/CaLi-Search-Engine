from plotly.offline import plot
from plotly.graph_objs import Scatter3d, Line, Marker, XAxis, YAxis, ZAxis, Layout, Scene, Data, Figure


def generate_coordinate(lattice, width, height):
    x = width
    y = height
    z = 0

    Xn = [width/2]
    Yn = [y]
    Zn = [z]

    Xe = []
    Ye = []
    Ze = []

    label = ['{}']
    terms = ['infimum']
    group = [1]

    x_node_space = width / 15
    y_node_space = x_node_space / 10
    for layer in lattice.set[1:]:
        y -= y_node_space
        margin = width - (width - len(layer) * x_node_space) / 2
        x = margin
        for license in layer:
            x -= x_node_space
            label.append("{}<br>{}".format(license.__repr__(), license.repr_terms()))
            terms.append(license.repr_terms())
            group.append(license.hash)
            Xn.append(x)
            Yn.append(y)
            Zn.append(z)
    return [Xn, Yn, Zn, Xe, Ye, Ze, label, group, terms]


def draw(lattice, width=1000, height=600):
    coordinates = generate_coordinate(lattice, width, height)

    trace1 = Scatter3d(x=coordinates[3],
                       y=coordinates[4],
                       z=coordinates[5],
                       mode='lines',
                       line=Line(color='rgb(50,50,50)', width=1),
                       hoverinfo='none')
    trace2 = Scatter3d(x=coordinates[0],
                       y=coordinates[1],
                       z=coordinates[2],
                       mode='markers',
                       name=coordinates[8],
                       marker=Marker(symbol='dot',
                                     size=6,
                                     color=coordinates[7],
                                     colorscale='Paired',
                                     line=Line(color='rgb(50,50,50)', width=0.5)),
                       text=coordinates[6],
                       hoverinfo='text')

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    layout = Layout(
         title="CaLi",
         width=width,
         height=height,
         showlegend=False,
         scene=Scene(
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            zaxis=ZAxis(axis),
         ),
         hovermode='closest')

    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)

    plot(fig, filename='CaLi_visualisation.html')
