import numpy as np
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("./resource_usage.csv")

starting_points = [0] * len(df)
for i, s in enumerate(starting_points):
    starting_points[i] = sum(df["cpuhour"][:i])
y = np.arange(len(df)) * 0.05
fig = go.Figure()
fig.add_trace(
    go.Bar(
        y=y,
        x=df["cpuwait"],
        base=starting_points,
        name="CPU Wait",
        orientation="h",
        marker_color="firebrick",
    )
)
fig.add_trace(
    go.Bar(
        y=y,
        x=list(df["cpuused"]),
        base=[s + w for s, w in zip(starting_points, df["cpuwait"])],
        name="CPU used",
        orientation="h",
        marker_color="steelblue",
    )
)

fig.update_traces(width=0.025)
fig.update_layout(
    title="Lockman A processing cost",
    width=int(2 * 300 * 10 / 3),
    font=dict(size=32),
    xaxis_title="CPU hours consumed",
    yaxis_title="",
    barmode="stack",
    bargap=0.05,
)
fig.update_yaxes(
    tickmode="array", tickvals=y, ticktext=list(df["step"]), autorange="reversed"
)
fig.write_image("resource_usage.png")
