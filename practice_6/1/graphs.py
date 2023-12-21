import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv')


def days_of_week():
    plt.clf()
    graph = df['day_of_week'].value_counts().plot(kind='bar', title='matches by day of week', figsize=(10, 6))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('days_of_week.png')


def days_of_week_other_view():
    plt.clf()
    graph = df['day_of_week'].value_counts().plot(kind='pie', title='matches by day of week', autopct='%1.1f%%')
    graph.yaxis.label.set_visible(False)
    graph.figure.savefig('days_of_week_pie.png')


def correlation():
    plt.clf()
    _df = df.copy().select_dtypes(include=['int'])
    plt.figure(figsize=(16, 16))
    figure = sns.heatmap(_df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    figure.get_figure().savefig('correlation.png')


def errors():
    plt.clf()
    groups = df.groupby('h_manager_name')['h_errors'].sum().sort_index(ascending=False).head(10)
    groups.plot(kind='bar', title='errors')
    plt.savefig('errors.png')


def length():
    plt.clf()
    df.groupby('day_of_week')['length_minutes'].mean().plot()
    plt.xlabel('День недели', labelpad=50)
    plt.ylabel('Средняя продолжительность в минутах', labelpad=50)
    plt.savefig('length.png')


days_of_week()
days_of_week_other_view()
correlation()
errors()
length()
