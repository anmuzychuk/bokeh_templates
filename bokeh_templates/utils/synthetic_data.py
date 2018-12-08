import numpy as np
import pandas as pd


def generate_data(seed=1234):

    np.random.seed(seed)
    # generate some synthetic time series for six different categories
    cats = list("abcdef")
    yy = np.random.randn(2000)
    g = np.random.choice(cats, 2000)
    for i, l in enumerate(cats):
        yy[g == l] += i // 2
    df = pd.DataFrame(dict(score=yy, group=g))

    return df
