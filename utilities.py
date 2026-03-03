import nfl_data_py as nfl

# Define distance buckets
def yards_to_go_bucket(x):
    """
    Converts numerical yards to go into buckets of short yardage, medium yardage,
    and long yardage.
    :param x:
    :return:
    """
    if x <= 3:
        return 'short'
    elif x <= 7:
        return 'medium'
    else:
        return 'long'


# Get list of teams
def fetch_list_of_teams():
    # Get most recent year
    pbp = nfl.import_pbp_data([2025])

    teams = (
        pbp['posteam']
        .dropna()
        .unique()
    )

    return sorted(teams)
