import dash
import plotly.graph_objects as go
from dash import dcc, html

from support import read_file_raw

sample = read_file_raw(__file__, "../../input/2022/18/sample.txt")
puzzle = read_file_raw(__file__, "../../input/2022/18/puzzle.txt")

x = []
y = []
z = []

for line in puzzle.splitlines():
    x1, y1, z1 = map(int, line.split(","))
    x.append(x1)
    y.append(y1)
    z.append(z1)

fig = go.Figure(
    data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker=dict(
                size=6,
                color=x,
                colorscale="Viridis",
                opacity=0.8,
            ),
        )
    ]
)

fig.update_layout(scene=dict(xaxis_showspikes=False, yaxis_showspikes=False))

app = dash.Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])

app.run_server(debug=True, use_reloader=True)
