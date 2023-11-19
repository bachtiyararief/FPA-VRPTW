import plotly.express as px
import plotly.graph_objects as go

def plot_pergerakan_fungsi_tujuan(y):
    x = range(1, len(y)+1, 1)
    fig = px.line(
        x = x,
        y = y,
        labels = {'x': 'Iterasi', 'y': 'Total Jarak'},
        markers = True,
        color_discrete_sequence = ['#541675']
    )
    
    fig.update_layout(
        height = 650,
        width = 1200,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        yaxis = dict(
            title = 'Total Jarak',
            showline = True,
            linewidth = 1,
            color = '#7E38B7',
            linecolor = '#7E38B7'
        ),
        xaxis = dict(
            range = [1, len(y)],
            title = 'Iterasi',
            showline = True,
            linewidth = 1,
            color = '#7E38B7',
            linecolor = '#7E38B7'
        )
    )
    
    fig.update_xaxes(
        tickmode = 'linear', 
        dtick = 1
    )

    return(fig)

def plot_rute_vrptw(data_coord, rute):
    nodes = dict()
    for key, value in data_coord[['Coord. X', 'Coord. Y']].to_dict('index').items():
        if(key == 0):
            nodes.update({'Depot' : (value.get('Coord. X'), value.get('Coord. Y'))})
        else:
            nodes.update({f'Customer {key}' : (value.get('Coord. X'), value.get('Coord. Y'))})
    
    routes = list()
    for i in rute['Rute'].tolist():
        r = list(map(lambda x: 'Depot' if x == 0 else f'Customer {x}', i))
        routes.append(r)

    """
    fig = go.Figure()
    for node, (x, y) in nodes.items():
        fig.add_trace(
            go.Scatter(
                x = [x], 
                y = [y], 
                mode = 'markers', 
                text = [node], 
                name = node
            )
        )
    
    i = 0
    for route in routes:
        x = [nodes[node][0] for node in route]
        y = [nodes[node][1] for node in route]
        x.append(x[0])
        y.append(y[0])
        fig.add_trace(
            go.Scatter(
                x = x, 
                y = y, 
                mode = 'lines', 
                name = 'Route'
            )
        )
        i += 1
    
    # Update layout
    fig.update_layout(
        title = 'Rute Terbaik Vehicle Routing Problem with Time Windows <sup>Pada Hasil Perhitungan FPA</sup>',
        xaxis = dict(title = 'X'),
        yaxis = dict(title = 'Y'),
        height = 650,
        width = 1200,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        showlegend = False,
        hovermode = 'closest'
    )
    """
    
    return(nodes, routes)
