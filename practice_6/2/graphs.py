import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv')


def brands():
    plt.clf()
    graph = df['brandName'].value_counts().plot(kind='bar', title='cars by brand', figsize=(10, 12))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('brands.png')


def correlation():
    plt.clf()
    _df = df.copy().select_dtypes(include=['int', 'float'])
    plt.figure(figsize=(16, 16))
    figure = sns.heatmap(_df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    figure.get_figure().savefig('correlation.png')


def vehicle_types():
    plt.clf()
    graph = df['vf_VehicleType'].value_counts().plot(kind='pie', title='cars by vehicle type', autopct='%1.1f%%')
    graph.yaxis.label.set_visible(False)
    graph.figure.savefig('vehicle_types.png')


def price_by_brand():
    plt.clf()
    groups = df.groupby('brandName')['askPrice'].mean().sort_index(ascending=False).head(10)
    groups.plot(kind='bar')
    plt.savefig('price_by_brand.png')


def seats():
    plt.clf()
    graph = df['vf_Seats'].value_counts().plot(kind='bar', title='cars by seats')
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('seats.png')


brands()
correlation()
vehicle_types()
price_by_brand()
seats()
