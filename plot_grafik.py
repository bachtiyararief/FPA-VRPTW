import plotly.express as px
import pandas as pd

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
            linecolor = '#7E38B7',
            tickmode = 'linear',
            dtick = 10
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

    max_routes = 0
    routes = list()
    for i in rute:
        r = list(map(lambda x: 'Depot' if x == 0 else f'Customer {x}', i))
        if(max_routes <= len(r)):
            max_routes = len(r)
        routes.append(r)

    nodes_df = pd.DataFrame(list(nodes.values()), columns=['X', 'Y'], index=nodes.keys())
    routes_df = pd.DataFrame(routes, columns=[f'Node_{i}' for i in range(1, max_routes+1)])
    
    fig = px.scatter(nodes_df, x='X', y='Y', text=nodes_df.index, title='Vehicle Routing Problem with Time Windows')
    color = px.colors.sequential.Plasma_r + px.colors.sequential.Turbo_r + px.colors.sequential.Viridis
    for i in range(len(routes_df)):
        route = routes_df.iloc[i].dropna().tolist()
        route.append(route[0])  # To close the loop
        fig.add_trace(px.line(nodes_df.loc[route], x='X', y='Y', color_discrete_sequence=[color[i]]).data[0])

    fig.update_layout(
        height = 650,
        width = 1200,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        showlegend = False,
        hovermode = 'closest'
    )

    return(fig)
