import nfl_data_py as nfl
import pandas as pd
import numpy as np


# Load 2025 play-by-play data
pbp = nfl.import_pbp_data([2025])

# Keep only offensive pass and run plays
pbp = pbp[
    (pbp['play_type'].isin(['pass', 'run']) &
     (pbp['epa'].notna()))
].copy()

