from operator import index

from Tools.scripts.make_ctype import values
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output
)
import plotly.express as px
import plotly.graph_objects as go
from numpy.ma.extras import column_stack

from examples.epa_dashboard.epa_dashboard_dataframes import team_play_type_distribution
from utilities import fetch_list_of_teams
from epa_dashboard_dataframes import (
    team_vs_league_epa,
    team_play_type_distribution,
    league_play_type_distribution
)

app = Dash(__name__)

teams = fetch_list_of_teams()

# App layout
app.layout = html.Div([

    html.H1("2025 Offensive EPA Dashboard"),

    dcc.Dropdown(
        id='team-dropdown',
        options=[{
            'label': t,
            'value': t
        } for type in teams
        ]
    ),

    html.Div([
        dcc.Graph(id='pass-heatmap'),
        dcc.Graph(id='rush-heatmap')
    ], style={'display': 'flex'}),

    dcc.Graph(id='distribution-bar')
])

# Callbacks
@app.callback(
    Output('pass-heatmap', 'figure'),
    Output('rush-heatmap', 'figure'),
    Output('distribution-bar', 'figure'),
    Input('team-dropdown', 'value')
)

# Updating dashboard after a team is selected
def update_dashoard(selected_team):

    # Set the team to view
    team_data = team_vs_league_epa[
            team_vs_league_epa['posteam'] == selected_team
    ]

    # Pass heatmap
    pass_df = team_data[
        team_data['play_type'] == 'pass'
    ]

    pass_pivot = pass_df.pivot(
        index='down',
        columns='yards_to_go_bucket',
        values='epa_diff'
    )

    # Create the passing epa heatmap
    pass_fig = px.imshow(
        pass_pivot,
        color_continuous_scale='RdBu',
        origin='lower',
        title=f'{selected_team} Passing EPA vs League'
    )

    # Rush heatmap
    rush_df = team_data[
        team_data['play_type'] == 'run'
        ]

    rush_pivot = rush_df.pivot(
        index='down',
        columns='yards_to_go_bucket',
        values='epa_diff'
    )

    # Create the rushing epa heatmap
    rush_fig = px.imshow(
        rush_pivot,
        color_continuous_scale='RdBu',
        origin='lower',
        title=f'{selected_team} Rushing EPA vs League'
    )

    # Play Type Distribution Bar Chart
    team_dist = team_play_type_distribution[
        team_play_type_distribution['posteam'] == selected_team
    ]

    bar_fig = go.Figure()

    bar_fig.add_trace(
        go.Bar(
            x=team_dist['team_pct'],
            y=team_dist['play_type'],
            orientation='h',
            name=selected_team
        )
    )

    # League reference lines
    for _, row in league_play_type_distribution.iterrows():
        bar_fig.add_vline(
            x=row['league_pct'],
            line_dash='dash'
        )

    bar_fig.update_layout(
        title="Play Type Distribution (Team vs League Avg)"
    )

    return pass_fig, rush_fig, bar_fig

if __name__ == "__main__":
    app.run_server(debug=True)