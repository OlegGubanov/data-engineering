import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv', low_memory=False)


def years():
    plt.clf()
    graph = df['YEAR'].value_counts().plot(kind='bar', title='flights by year', figsize=(10, 12))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('years.png')


def correlation():
    plt.clf()
    _df = df.copy().select_dtypes(include=['int', 'float'])
    plt.figure(figsize=(16, 16))
    figure = sns.heatmap(_df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    figure.get_figure().savefig('correlation.png')


def cancelled():
    plt.clf()
    graph = df['CANCELLED'].value_counts().plot(kind='pie', title='flights', autopct='%1.1f%%')
    graph.yaxis.label.set_visible(False)
    graph.figure.savefig('cancelled.png')


def delay_by_airport():
    plt.clf()
    groups = df.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().sort_index(ascending=False).head(10)
    groups.plot(kind='bar')
    plt.savefig('delay.png')


def airlines():
    plt.clf()
    graph = df['AIRLINE'].value_counts().plot(kind='bar', title='airlines', figsize=(10, 12))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('airlines.png')


years()
correlation()
cancelled()
delay_by_airport()
airlines()
