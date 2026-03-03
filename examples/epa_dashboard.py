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

x = 1