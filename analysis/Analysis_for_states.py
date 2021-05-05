from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def get_line_chart( file, state):
    df = pd.read_csv( file )
    df2 = df.loc[ df["state"] == state]
    df2 = df2.reset_index(drop=True)

    df2["new_cases"] = 0
    df2["new_cases"].iloc[0] = df2["cases"].iloc[0]
    for i in range(1, len(df2)):
        df2["new_cases"].iloc[i] = df2["cases"].iloc[i] - df2["cases"].iloc[i-1]

    df2["newdate"] = ""
    for i in range(len(df2)):
        df2["newdate"].iloc[i] = df2["date"].iloc[i][:10] 
    
    df2 = df2.set_index( pd.DatetimeIndex( df2["newdate"].values))
    
    column_list = ["retail_and_recreation_percent_change_from_baseline",\
               "grocery_and_pharmacy_percent_change_from_baseline", \
#               "parks_percent_change_from_baseline",\
               "transit_stations_percent_change_from_baseline",\
               "workplaces_percent_change_from_baseline",\
               "residential_percent_change_from_baseline"]

    print("Seperate Line Charts: ")
    df2[column_list].plot(figsize = (6, 5))
    plt.title( "Line Chart for all indicators")
    plt.ylabel( "Percentage Change")
    plt.xlabel( "Date")
    plt.show()

    df2["new_cases"].plot(figsize = (6, 5))
    plt.title( "Line Chart for new Cases")
    plt.ylabel( "numbers")
    plt.xlabel( "Date")
    plt.show()
    
    retail = np.array(df2["retail_and_recreation_percent_change_from_baseline"])
    grocery = np.array(df2["grocery_and_pharmacy_percent_change_from_baseline"])
    transit = np.array( df2["transit_stations_percent_change_from_baseline"])
    workplace = np.array(df2["workplaces_percent_change_from_baseline"])
    resident = np.array(df2["residential_percent_change_from_baseline"])

    cases = np.array(df2["new_cases"])
    days2 = np.array( df2["newdate"])
    days = []
    for day in days2:
        days.append(datetime.strptime(day, '%Y-%m-%d'))
    
    print("Combined Line Chart with 2 y axis: ")
    print( "    Red:    retail_and_recreation_percent_change_from_baseline, y_axis on the left")
    print( "    blue:   grocery_and_pharmacy_percent_change_from_baseline,  y_axis on the left")
    print( "    brown:  transit_stations_percent_change_from_baseline,      y_axis on the left")
    print( "    green:  workplaces_percent_change_from_baseline,            y_axis on the left")
    print( "    orange: residential_percent_change_from_baseline,           y_axis on the left")
    print( "    black:  new cases,                                          y_axis on the right")
    print()
    print( "Y_label for the y_axis on the left is percent change from baseline")
    print( "Y_label for the y_axis on the right is number of cases")
    
    fig, ax1 = plt.subplots(figsize = (6, 5) )
    ax1.plot(days, retail, linewidth=2, color="red" )
    ax1.plot(days, grocery, linewidth=2, color="blue")
    ax1.plot(days, transit, linewidth=2, color="brown")
    ax1.plot(days, workplace, linewidth=2, color="green" )
    ax1.plot(days, resident, linewidth=2, color="orange")


    ax2= ax1.twinx()
    ax2.plot( days, cases, linewidth=2, color="black")
    fig.tight_layout()
    plt.show()


def get_bar_chart( file, state):
    df = pd.read_csv( file)
    df2 = df.loc[ df["state"] == state]
    df2 = df2.reset_index(drop=True)

    df2["new_cases"] = 0
    df2["new_cases"].iloc[0] = df2["cases"].iloc[0]
    for i in range(1, len(df2)):
        df2["new_cases"].iloc[i] = df2["cases"].iloc[i] - df2["cases"].iloc[i-1]

    df2["newdate"] = ""
    for i in range(len(df2)):
        df2["newdate"].iloc[i] = df2["date"].iloc[i][:10] 
    
    df2 = df2.set_index( pd.DatetimeIndex( df2["newdate"].values))
    
    column_list = ["retail_and_recreation_percent_change_from_baseline",\
               "grocery_and_pharmacy_percent_change_from_baseline", \
#               "parks_percent_change_from_baseline",\
               "transit_stations_percent_change_from_baseline",\
               "workplaces_percent_change_from_baseline",\
               "residential_percent_change_from_baseline"]
    
    retail = np.array(df2["retail_and_recreation_percent_change_from_baseline"])
    grocery = np.array(df2["grocery_and_pharmacy_percent_change_from_baseline"])
    transit = np.array( df2["transit_stations_percent_change_from_baseline"])
    workplace = np.array(df2["workplaces_percent_change_from_baseline"])
    resident = np.array(df2["residential_percent_change_from_baseline"])

    cases = np.array(df2["new_cases"])
    days2 = np.array( df2["newdate"])
    days = []
    for day in days2:
        days.append(datetime.strptime(day, '%Y-%m-%d'))
    
    r_g = np.add(retail, grocery).tolist()
    r_g_t = np.add( r_g, transit)
    r_g_t_w = np.add( r_g_t, workplace)
    total=np.add( r_g_t_w, retail)
    
    plt.bar(days, retail, label = "retail")
    plt.bar(days, grocery, bottom=retail, label="grocery")
    plt.bar(days, transit, bottom=r_g, label="transit")
    plt.bar(days, workplace, bottom=r_g_t, label="workplace")
    plt.bar(days, resident, bottom=r_g_t_w, label="resident")
    
    plt.xlabel("Date")
    plt.ylabel("Percentage Change")
    plt.legend()
    plt.title( "Stacked bar chart for indicators")
    plt.show()

    plt.bar(days, cases, label = "cases")
    plt.xlabel("Date")
    plt.ylabel("Percentage Change")
    plt.legend()
    plt.title( "Bar chart for cases")
    plt.show()


def get_weekly( file, state, period):
    df = pd.read_csv( file)
    df2 = df.loc[ df["state"] == state]
    df2 = df2.reset_index(drop=True)

    df2["new_cases"] = 0
    df2["new_cases"].iloc[0] = df2["cases"].iloc[0]
    for i in range(1, len(df2)):
        df2["new_cases"].iloc[i] = df2["cases"].iloc[i] - df2["cases"].iloc[i-1]

    df2["newdate"] = ""
    for i in range(len(df2)):
        df2["newdate"].iloc[i] = df2["date"].iloc[i][:10] 
    
    df2 = df2.set_index( pd.DatetimeIndex( df2["newdate"].values))
    
    weeks = len(df2) // period
    week = []
    retail = []
    grocery = []
    transit = []
    workplace = []
    resident = []
    cases = []

    for i in range( weeks):
        total = []
        total_retail = 0
        total_grocery = 0
        total_transit = 0
        total_workspaces = 0
        total_residential = 0
        total_cases = 0
        for j in range(period):
            total_retail      += df2["retail_and_recreation_percent_change_from_baseline"].iloc[i*period+j]
            total_grocery     += df2["grocery_and_pharmacy_percent_change_from_baseline"].iloc[i*period+j]
            total_transit     += df2["transit_stations_percent_change_from_baseline"].iloc[i*period+j]
            total_workspaces  += df2["workplaces_percent_change_from_baseline"].iloc[i*period+j]
            total_residential += df2["residential_percent_change_from_baseline"].iloc[i*period+j]
            total_cases       += df2["new_cases"].iloc[i*period+j]
        week.append( i )
        retail.append( total_retail/period )
        grocery.append( total_grocery/period)
        transit.append( total_transit/period)
        workplace.append( total_workspaces/period)
        resident.append( total_residential/period)
        cases.append( total_cases/period)
    

    
    print("Combined Line Chart with 2 y axis: ")
    print( "    Red:    retail_and_recreation_percent_change_from_baseline, y_axis on the left")
    print( "    blue:   grocery_and_pharmacy_percent_change_from_baseline,  y_axis on the left")
    print( "    brown:  transit_stations_percent_change_from_baseline,      y_axis on the left")
    print( "    green:  workplaces_percent_change_from_baseline,            y_axis on the left")
    print( "    orange: residential_percent_change_from_baseline,           y_axis on the left")
    print( "    black:  new cases,                                          y_axis on the right")
    print()
    print( "X_label is number of weeks from baseline")
    print( "Y_label for the y_axis on the left is percent change from baseline")
    print( "Y_label for the y_axis on the right is number of cases")
    
    fig, ax1 = plt.subplots(figsize = (6, 5) )
    ax1.plot(week, retail, linewidth=2, color="red" )
    ax1.plot(week, grocery, linewidth=2, color="blue")
    ax1.plot(week, transit, linewidth=2, color="brown")
    ax1.plot(week, workplace, linewidth=2, color="green" )
    ax1.plot(week, resident, linewidth=2, color="orange")


    ax2= ax1.twinx()
    ax2.plot( week, cases, linewidth=2, color="black")
    fig.tight_layout()
    plt.title("Combined Chart for weekly data: ")
    plt.show()
    
    r_g = np.add(retail, grocery).tolist()
    r_g_t = np.add( r_g, transit)
    r_g_t_w = np.add( r_g_t, workplace)
    total=np.add( r_g_t_w, retail)
    
    plt.bar(week, retail, label = "retail")
    plt.bar(week, grocery, bottom=retail, label="grocery")
    plt.bar(week, transit, bottom=r_g, label="transit")
    plt.bar(week, workplace, bottom=r_g_t, label="workplace")
    plt.bar(week, resident, bottom=r_g_t_w, label="resident")
    
    plt.xlabel("Weeks from Baseline")
    plt.ylabel("Percentage Change")
    plt.legend()
    plt.title( "Stacked bar chart for indicators")
    plt.show()

    plt.bar(week, cases, label = "cases")
    plt.xlabel("Weeks from Baseline")
    plt.ylabel("Percentage Change")
    plt.legend()
    plt.title( "Bar chart for cases")
    plt.show()

  