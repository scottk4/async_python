import pandas as pd

def make_dataframe(data, sortby_col):
    df = pd.DataFrame(data)
    return df.sort_values(by=sortby_col, ascending=False)
