import plotly.express as px

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
