from bokeh_templates.utils import Summary, generate_data
import numpy as np

df = generate_data()
print(df.head())


# summmarise 1d array:
x = np.random.randn(2000)
smr = Summary.summarize_x(x)
print(f"1d array summary: \n{smr}")

# summize each category level separately
for category in df['group'].unique():
    print(f"Summary for category {category}:")
    print("-" * 80)
    x = df.loc[df['group'] == category, 'score']
    print(Summary.summarize_x(x))
    print("-" * 80)
    print()


score_summary = Summary(df, 'group', 'score')
print(score_summary)


print(score_summary.summary_table)


print(score_summary.outliers)
