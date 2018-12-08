"""
Summary class to provide a quick access to statistical summary
in a way useful to create box-plot.

"""

import numpy as np
import pandas as pd


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
        dx = pd.concat(dx)
        dx.rename(columns={"category": self.key}, inplace=True)
        return dx

    def outliers(self):
        """Retrurns outliers, if any."""
        # if not self.summary:
        #     self.summary = self.summarize()

        dx = pd.merge(self.df[[self.key, self.xval]],
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
        dx = pd.DataFrame({
            "category": category_value,
            "min": [np.min(x)],
            "q1": [np.quantile(x, 0.25)],
            "median": [np.quantile(x, 0.5)],
            "q3": [np.quantile(x, 0.75)],
            "max": [np.max(x)]
        })

        dx['iqr'] = dx['q3'] - dx['q1']
        dx['upper'] = dx['q3'] + k * dx['iqr']
        dx['lower'] = dx['q1'] - k * dx['iqr']
        dx['stem_upper'] = dx[['upper', 'max']].apply(min, axis=1)
        dx['stem_lower'] = dx[['lower', 'min']].apply(max, axis=1)
        return dx
