import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv', low_memory=False)


def years():
    plt.clf()
    graph = df['year'].value_counts().head(10).plot(kind='pie', autopct='%1.1f%%', figsize=(19, 10))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('years.png')


def manufacturers():
    plt.clf()
    graph = df['manufacturer'].value_counts().head(10).plot(kind='bar')
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('manufacturers.png')


def price_by_year():
    plt.clf()
    groups = df.groupby('year')['price'].mean().sort_index(ascending=False).head(10)
    groups.plot(kind='bar')
    plt.savefig('price_by_year.png')


def cylinders():
    plt.clf()
    graph = df['cylinders'].value_counts().plot(kind='bar')
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('cylinders.png')


def price_by_model():
    plt.clf()
    groups = df.groupby('model')['price'].mean().sort_index(ascending=False).head(5)
    groups.plot()
    plt.savefig('price_by_model.png')


years()
manufacturers()
price_by_year()
cylinders()
price_by_model()
