import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv', low_memory=False)


def correlation():
    plt.clf()
    _df = df.copy().select_dtypes(include=['int', 'float'])
    plt.figure(figsize=(16, 16))
    figure = sns.heatmap(_df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    figure.get_figure().savefig('correlation.png')


def classes():
    plt.clf()
    graph = df['class'].value_counts().plot(kind='bar')
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('class.png')


def diameter():
    plt.clf()
    groups = df.groupby('class')['diameter'].mean()
    groups.plot(kind='bar')
    plt.savefig('diameter.png')


def albedo():
    plt.clf()
    groups = df.groupby('name')['diameter'].mean().sort_index(ascending=False).head(10)
    groups.plot(kind='bar')
    plt.savefig('albedo.png')


def epoch():
    plt.clf()
    groups = df.groupby('class')['epoch_cal'].mean().sort_index()
    groups.plot()
    plt.savefig('epoch.png')


correlation()
classes()
diameter()
albedo()
epoch()
