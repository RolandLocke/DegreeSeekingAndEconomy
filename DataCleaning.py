"""
Roland Locke
2/3/24

Methods for cleaning data and displaying data, using this document to plan out the data cleaning necessary for this
project.

making plots look nice:https://www.easytweaks.com/matplotlib-seaborn-text-label-points/
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def number_of_applicants_over_time():
    # # Print the number_of_applicants_over_time graph
    # applicantsGraph = number_of_applicants_over_time()
    # applicantsGraph.show()

    #CREATING A GRAPH WITH MATPLOTLIB
    #this needs to be applied to each of the columns or the red_csv function needs to take in floats not strings
    applicantValues = df1.loc[:, 'Number applicants'].str.replace(',', '').astype(float)
    admittedValues = df1.loc[:, 'Number admitted'].str.replace(',', '').astype(float)
    xValues = df1.loc[:, 'Date']

    # create the line graph
    plt.plot(xValues, applicantValues, label='Number of applicants', color='blue', linestyle='-', linewidth=2)
    plt.plot(xValues, admittedValues, label='Number admitted', color='red', linestyle='-', linewidth=2)

    #add key
    plt.gca().legend()

    # remove the scientific notation
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    # set the y axis limits
    plt.ylim(3000000, 14000000)

    # add gridlines
    plt.grid()

    return plt

def scatter_applicants_vs_cci_over_time():

    # CCIApplicantsGraph = scatter_applicants_vs_cci_over_time()
    # CCIApplicantsGraph.show()

    applicantValues = df1.loc[:, 'Applicants Percent Change']
    CCI = df1['CCI Percent Change']
    xValues = df1.loc[:, 'Date']

    plt.scatter(xValues, applicantValues, label='Number of Applicants', color='blue')
    plt.scatter(xValues, CCI, label='CCI', color='Red')

    # add key set axis titles
    plt.ylabel('Percent Change')
    plt.xlabel('Time')
    plt.gca().legend()

    # ensures dates are displayed individually, not as float values
    plt.gca().set_xticks(df1["Date"].unique())

    return plt

def scatter_applicants_vs_cci_over_time():

    # CCIApplicantsGraphScaled = scaled_scatter_applicants_vs_cci_over_time()
    # CCIApplicantsGraphScaled.show()

    # assign the values
    applicants = df1['Number applicants']
    CCI = df1['CCI']

    # plot the graph
    plt.scatter(CCI, applicants, label='Number of Applicants', color='blue')

    # add key set axis titles
    plt.xlabel('CCI')
    plt.ylabel('Applicants')

    # add labels to the points on the graph
    for i, txt in enumerate(df1['Date']):
        plt.annotate(txt, (CCI[i], applicants[i]))

    return plt

# admission and application data
df1 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\admissions_applications.csv", thousands=',')

# consumer confidence index, Time Series
df2 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\CCI.csv", on_bad_lines='skip')

# Consumer Price Index, Time Series
df3 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\CPI.csv", on_bad_lines='skip')

# Employment Level
df4 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\Employment.csv", on_bad_lines='skip')

# GDP
df5 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\GDP.csv", on_bad_lines='skip')

# inflation
df6 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\inflation.csv", on_bad_lines='skip')

# Unemployment rate
df7 = pd.read_csv("C:\\Users\\rolan\\IdeaProjects\\DegreeSeekingUndergraduateIsAndEconomy\\Datasets\\UNRATE.csv", on_bad_lines='skip')

#======================================================================================================================
# create a dataframe to hold Admission and Application data

#remove the first column
df1 = df1.iloc[:, 1:]

# change the first column name to 'date'
df1.columns = df1.columns.to_series().replace({'Unnamed: 1': 'Date'}).tolist()

# .T the transpose function creates a new dataframe where the rows become columns and vise versa
df1 = df1.T

# Make the labels the new column values:
df1.columns = df1.iloc[0]
df1 = df1.iloc[1:]

# reset the index values
df1 = df1.reset_index()

# ensure the first column is name date
df1.columns = df1.columns.to_series().replace({'Date': 'index'}).tolist()
df1.columns = df1.columns.to_series().replace({'index': 'Date'}).tolist()

# reverse the order of the row columns
df1 = df1.iloc[::-1]

# set Date to hold int values, important for eventual merges
df1['Date'] = df1['Date'].astype(int)

# ======================================================================================================================
# adding percent change for applicants

number_applicants_as_float = df1.iloc[:, 1].str.replace(',', '').astype(float)

applicants_percent_change = number_applicants_as_float.pct_change() * 100

df1.insert(2, "Applicants Percent Change", applicants_percent_change, True)

# ======================================================================================================================
# Consumer Confidence Index

# remove all but the USA data
df2 = df2[df2['LOCATION'] == 'USA']

# remove un-needed columns
df2 = df2.iloc[:, 5:7]

# ensure the TIME column is an int value and remove the month metric
df2['TIME'] = df2['TIME'].apply(lambda x: x[:4]).astype(int)

# this data is recorded monthly, so we need the mean CCI of each year
# group the data by year then find the mean()
df2grouped = df2.groupby(np.arange(len(df2))//12)
df2 = df2grouped.mean()

# rename TIME and Value columns to Date and CCI, set Date to hold int values, important for the eventual Merge
df2 = df2.rename(columns={'Value': 'CCI'})
df2 = df2.rename(columns={'TIME': 'Date'})
df2['Date'] = df2['Date'].astype(int)

# merge df1 and df2
df1 = df1.merge(df2, on='Date')

# ======================================================================================================================
# adding percent change for CCI
CCI_percent_change = df1['CCI'].pct_change() * 100

df1.insert(8, "CCI Percent Change", CCI_percent_change, True)

# ======================================================================================================================
# Consumer Price Index

# ensure the TIME column is an int value and remove the month metric
df3['DATE'] = df3['DATE'].apply(lambda x: x[:4]).astype(int)

# this data is recorded monthly, so we need the mean CPI of each year
# group the data by year then find the mean()
df3grouped = df3.groupby(np.arange(len(df3))//12)
df3 = df3grouped.mean()

# rename columns to Date and CPI, set Date to hold int values, important for an eventual Merge
df3 = df3.rename(columns={'USACPALTT01CTGYM': 'CPI'})
df3 = df3.rename(columns={'DATE':'Date'})
df3['Date'] = df3['Date'].astype(int)

# merge df1 and df3, with a left merge to perserve the years in df1 that dont exist in df3
df1 = df1.merge(df3, on='Date', how='left')

# ======================================================================================================================
# adding percent change for CPI
CPI_percent_change = df1['CPI'].pct_change() * 100

df1.insert(len(df1.columns), "CPI Percent Change", CPI_percent_change, True)

# Because CPI data doesn't start till 2011, we need to change the 0 values on the graph to NaN values
df1.loc[9, 'CPI Percent Change'] = None

# ======================================================================================================================
# Employment Level

# data is recorded in thousands, so convert them to
df4['CE16OV'] = df4['CE16OV'].apply(lambda x: x*1000).astype(int)

# ensure the TIME column is an int value and remove the month metric
df4['DATE'] = df4['DATE'].apply(lambda x: x[:4]).astype(int)

# this data is recorded monthly, so we need the mean Employment Level of each year
# group the data by year then find the mean()
df4grouped = df4.groupby(np.arange(len(df4))//12)
df4 = df4grouped.mean()

# rename columns, set Date to hold int values, important for the eventual Merge
df4 = df4.rename(columns={'CE16OV': 'Employment Level'})
df4 = df4.rename(columns={'DATE':'Date'})
df4['Date'] = df4['Date'].astype(int)

# merge df1 and df4, with a left merge
df1 = df1.merge(df4, on='Date', how='left')

# ======================================================================================================================
# adding percent change for Employment Level
Employment_percent_change = df1['Employment Level'].pct_change() * 100

df1.insert(len(df1.columns), "Employment level Percent Change", Employment_percent_change, True)

# ======================================================================================================================
# GDP

# ensure the TIME column is an int value and remove the month metric
df5['DATE'] = df5['DATE'].apply(lambda x: x[:4]).astype(int)

# this data is recorded monthly, so we need the mean Employment Level of each year
# group the data by year then find the mean()
df5grouped = df5.groupby(np.arange(len(df5))//4)
df5 = df5grouped.mean()

# rename column, set Date to hold int values, important for the eventual Merge
df5 = df5.rename(columns={'DATE':'Date'})
df5['Date'] = df5['Date'].astype(int)

# merge df1 and df5, with a left merge
df1 = df1.merge(df5, on='Date', how='left')

# ======================================================================================================================
# adding percent change for GDP
GDP_percent_change = df1['GDP'].pct_change() * 100

df1.insert(len(df1.columns), "GDP Percent Change", GDP_percent_change, True)

# ======================================================================================================================
# Inflation

# ensure the TIME column is an int value and remove the month metric
df6['DATE'] = df6['DATE'].apply(lambda x: x[:4]).astype(int)

# rename columns to Date and CPI, set Date to hold int values, important for an eventual Merge
df6 = df6.rename(columns={'FPCPITOTLZGUSA': 'Inflation'})
df6 = df6.rename(columns={'DATE':'Date'})
df6['Date'] = df6['Date'].astype(int)

# merge df1 and df6, with a left merge to perserve the years in df1 that dont exist in df3
df1 = df1.merge(df6, on='Date', how='left')

# ======================================================================================================================
# adding percent change for Inflation
Inflation_percent_change = df1['Inflation'].pct_change() * 100

df1.insert(len(df1.columns), "Inflation Percent Change", Inflation_percent_change, True)
# ======================================================================================================================
# Unemployment Rate

# remove the month metric
df7['DATE'] = df7['DATE'].apply(lambda x: x[:4]).astype(int)

# this data is recorded monthly
# group the data by year then find the mean()
df7grouped = df7.groupby(np.arange(len(df7))//12)
df7 = df7grouped.mean()

df7 = df7.rename(columns={'DATE': 'Date'})
df7['Date'] = df7['Date'].astype(int)

df1 = df1.merge(df7, on='Date')

# ======================================================================================================================
# adding percent change for UNRATE
UNRATE_percent_change = df1['UNRATE'].pct_change() * 100

df1.insert(len(df1.columns), "UNRATE Percent Change", UNRATE_percent_change, True)
# ======================================================================================================================

# here you can explore some of the out
# print(df1)

df1.to_csv("Economy_and_degree.csv", sep=',', index=False, encoding='utf-8')

# ======================================================================================================================
# scaling data
# data should be scaled to easily compare
dfScaled = df1.loc[:, 'Applicants Percent Change'].to_frame()
dfScaled['CCI Percent Change'] = df1['CCI Percent Change']

# Initialize the scikit-learn MinMaxScaler
scaler = MinMaxScaler(feature_range=(-1, 1))
# Scale the data
dfScaled = pd.DataFrame(scaler.fit_transform(dfScaled), columns=dfScaled.columns)

# date was added later to prevent scaling the date
dfScaled.insert(0, 'Date', df1['Date'], True)
# ======================================================================================================================





                   