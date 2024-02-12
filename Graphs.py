"""
Roland Locke
2/12/24

In this document, the data collected in DataCleaning.py is graphed effectively.

making plots look nice:https://www.easytweaks.com/matplotlib-seaborn-text-label-points/
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df1 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Economy_and_degree.csv")

# ======================================================================================================================
# generate numerous graphs that will visualize a relationship between the percent change in applicants and the
# different economic indicators.

# create a list of column names to iterate over.
columns = df1.columns

for i in range(7, len(columns), 2):
    # assign the values
    applicants = df1['Applicants Percent Change']
    xVar = df1[columns[i]]

    # plot the graph
    plt.scatter(xVar, applicants, label='Applicants Percent Change', color='blue')

    # add key set axis titles
    plt.xlabel(columns[i])
    plt.ylabel('Number of Applicants Percent Change ')

    # add labels to the points on the graph
    for j, txt in enumerate(df1['Date']):
        plt.annotate(txt, (xVar[j], applicants[j]))

    plt.show()
