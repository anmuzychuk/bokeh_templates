import numpy
import pandas


def generate_data(seed=1234):

    numpy.random.seed(seed)
    # generate some synthetic time series for six different categories
    cats = list("abcdef")
    yy = numpy.random.randn(2000)
    g = numpy.random.choice(cats, 2000)
    for i, l in enumerate(cats):
        yy[g == l] += i // 2
    df = pandas.DataFrame(dict(score=yy, group=g))

    return df
