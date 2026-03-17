import nfl_data_py as nfl
import pandas as pd
import numpy as np

from utilities import yards_to_go_bucket

# Load 2025 play-by-play data
pbp = nfl.import_pbp_data([2025])

# Keep only offensive pass and run plays
pbp = pbp[
    (pbp['play_type'].isin(['pass', 'run']) &
     (pbp['epa'].notna()))
].copy()

# Yards to go bucket
pbp['yards_to_go_bucket'] = pbp['ydstogo'].apply(yards_to_go_bucket)

# League average epa by play type, down, and yards to go
league_avg_epa = (
    pbp
    .groupby(['play_type', 'down', 'yards_to_go_bucket'])
    .agg(
        league_epa=('epa', 'mean'),
    )
    .reset_index()
)

# Team average epa by team, play_type, down, and yards to go
team_avg_epa = (
    pbp
    .groupby(['posteam', 'play_type', 'down', 'yards_to_go_bucket'])
    .agg(
        team_epa=('epa', 'mean')
    )
    .reset_index()
)

# Merge league baseline
team_vs_league_epa = team_avg_epa.merge(
    league_avg_epa,
    on=['play_type', 'down', 'yards_to_go_bucket'],
    how='left'
)

# Calculate difference (team - league)
team_vs_league_epa['epa_diff'] = (
    team_vs_league_epa['team_epa'] -
    team_vs_league_epa['league_epa']
)

# Play type distribution for bar chart
team_play_type_distribution = (
    pbp
    .groupby(['posteam', 'play_type'])
    .size() # returns total number of elements it contains (play count)
    .reset_index(name='plays')
)

# Change distribution to percent
team_play_type_distribution['team_pct'] = (
    team_play_type_distribution.groupby('posteam')['plays']
    .transform(lambda x: x / x.sum())
)

# League play type distribution for bar chart
league_play_type_distribution = (
    pbp
    .groupby('play_type')
    .size() # returns total number of elements
    .reset_index(name='plays')
)

# Change distribution to percent
league_play_type_distribution['league_pct'] = (
    league_play_type_distribution['plays'] /
    league_play_type_distribution['plays'].sum()
)

x = 1