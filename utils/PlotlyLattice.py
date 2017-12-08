from plotly.offline import plot
from plotly.graph_objs import Scatter3d, Line, Marker, Margin, XAxis, YAxis, ZAxis, Annotation, Layout, Scene, Annotations, Font, Data, Figure


def generate_coordinate(lattice, x_node_space, y_node_space):
    x = 5
    y = 5
    z = 5

    Xn = []
    Yn = []
    Zn = []

    Xe = []
    Ye = []
    Ze = []

    label = []
    coordinate_parents(list(lattice.set[lattice.height()-1])[0], x, y, z, Xn, Yn, Zn, Xe, Ye, Ze, x_node_space, y_node_space, label)
    return [Xn, Yn, Zn, Xe, Ye, Ze, label]


def coordinate_parents(cl, x, y, z, Xn, Yn, Zn, Xe, Ye, Ze, x_node_space, y_node_space, label):
    label.append(cl.__repr__())
    Xn.append(x)
    Yn.append(y)
    Zn.append(z)

    Xe.append(x)
    Ye.append(y)
    Ze.append(z)
    Xe.append(None)
    Ye.append(None)
    Ze.append(None)
    for cpt, license in enumerate(cl.parents):
        Xe.append(x)
        Ye.append(y)
        Ze.append(z)
        if cpt % 2:
            coordinate_parents(license, x - x_node_space, y - y_node_space, z, Xn, Yn, Zn, Xe, Ye, Ze, x_node_space, y_node_space, label)
        else:
            coordinate_parents(license, x + x_node_space, y - y_node_space, z, Xn, Yn, Zn, Xe, Ye, Ze, x_node_space, y_node_space, label)


def draw(lattice, x_node_space, y_node_space):
    coordinates = generate_coordinate(lattice, x_node_space, y_node_space)

    trace1 = Scatter3d(x=coordinates[3],
                       y=coordinates[4],
                       z=coordinates[5],
                       mode='lines',
                       line=Line(color='rgb(125,125,125)', width=1),
                       hoverinfo='none')
    trace2 = Scatter3d(x=coordinates[0],
                       y=coordinates[1],
                       z=coordinates[2],
                       mode='markers',
                       name='actors',
                       marker=Marker(symbol='dot',
                                     size=6,
                                     colorscale='Viridis',
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
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
     margin=Margin(
        t=100
    ),
    hovermode='closest',
    annotations=Annotations([
           Annotation(
           showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=Font(
            size=14
            )
            )
        ]),    )

    data=Data([trace1, trace2])
    fig=Figure(data=data, layout=layout)

    plot(fig, filename='CaLi_visualisation.html')


def _generate_links_rec(cl):
    print cl
    for license in cl.parents:
        _generate_links_rec(license)
