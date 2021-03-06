"""
Summary class to provide a quick access to statistical summary
in a way useful to create box-plot.

"""

import numpy
import pandas


class Summary:

    def __init__(self, df, key, val, k=1.5):
        """
        :param df: a pandas data frame
        :param key: a column name (categorical)
        :param val: a column name (numerical)
        :param k: multiplier (to detect outliers), default to 1.5
        """
        self.df = df
        self.key = key
        self.xval = val
        self._k = k

        self.summary_table = self._summarize()
        self.outliers = self.outliers()

    def __str__(self):
        MSG = "Summary of {} by {}:\n{}\n{}\n{}"
        return MSG.format(self.xval, self.key, "-" * 100, self.summary_table, "-" * 100)

    def _summarize(self):
        """Wraps summarize_x method
        :param df: pandas data frame

        Return a summary table for each level of key column
        """
        groups = self.df[[self.key, self.xval]].groupby(self.key)
        dx = [Summary.summarize_x(x=dfx[self.xval],
                                  category_value=name,
                                  k=self._k)
              for name, dfx in groups]
        dx = pandas.concat(dx)
        dx.rename(columns={"category": self.key}, inplace=True)
        return dx

    def outliers(self):
        """Retrurns outliers, if any."""
        # if not self.summary:
        #     self.summary = self.summarize()

        dx = pandas.merge(self.df[[self.key, self.xval]],
                          self.summary_table[[self.key, 'upper', 'lower']],
                          how="left", on=self.key)
        outlier_ids = (dx[self.xval] > dx['upper']) | ((dx[self.xval] < dx['lower']))
        return dx[outlier_ids]

    @staticmethod
    def summarize_x(x, category_value="default", k=1.5):
        """Calculates base and extended summary

            base summary:
                min, q1, median, q3, max

            extended summary:
                iqr - Interquartile range
                upper - Upper bound for inliers
                lower - Lower bound for inliers
                stem_upper - Upper Steam(for box plot)
                steam_lower - Lower Steam value(for box plot)
        """

        # base summary
        dx = pandas.DataFrame({
            "category": category_value,
            "min": [numpy.min(x)],
            "q1": [numpy.percentile(x, 25)],
            "median": [numpy.percentile(x, 50)],
            "q3": [numpy.percentile(x, 75)],
            "max": [numpy.max(x)]
        })

        dx['iqr'] = dx['q3'] - dx['q1']
        dx['upper'] = dx['q3'] + k * dx['iqr']
        dx['lower'] = dx['q1'] - k * dx['iqr']
        dx['stem_upper'] = dx[['upper', 'max']].apply(min, axis=1)
        dx['stem_lower'] = dx[['lower', 'min']].apply(max, axis=1)
        return dx
