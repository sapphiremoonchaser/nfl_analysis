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
