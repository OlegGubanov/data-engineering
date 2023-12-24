import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('df.csv', low_memory=False)


def schedules():
    plt.clf()
    graph = df['schedule_name'].value_counts().plot(kind='bar', title='schedules', figsize=(10, 12))
    graph.xaxis.label.set_visible(False)
    graph.figure.savefig('schedules.png')


def premium():
    plt.clf()
    graph = df['premium'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    graph.yaxis.label.set_visible(False)
    graph.figure.savefig('premium.png')


def premium_salary():
    plt.clf()
    groups = df.groupby('premium')['salary_to'].mean()
    groups.plot(kind='bar')
    plt.savefig('premium_salary.png')


def salary_by_experience():
    plt.clf()
    groups = df.groupby('experience_name')['salary_to'].mean()
    groups.plot(kind='bar')
    plt.savefig('salary_by_experience.png')


def salary_by_employment():
    plt.clf()
    df.groupby('employment_name')['salary_to'].mean().plot()
    plt.savefig('salary_by_employment.png')


schedules()
premium()
premium_salary()
salary_by_experience()
salary_by_employment()
