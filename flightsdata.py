#IMPORTS
import sys
import pandas as pd

#OUTPUT FILE
sys.stdout = open('flightsdata_output.txt','w')

#DATAFRAMES
df_flights = pd.read_csv("flights.csv", header=0)
df_planes = pd.read_csv("planes.csv", header=0)

#FUNCTIONS
    #find sum of delays for given manufacturer
def manu_delay_sum(manufacturer):
    df_delay = df_flights[['manufacturer','arr_delay']].loc[df_flights['manufacturer'] == manufacturer]
    return(df_delay['arr_delay'].sum())

    #find count of delays for given manufacturer
def manu_delay_count(manufacturer):
    df_delay = df_flights[['manufacturer','arr_delay']].loc[df_flights['manufacturer'] == manufacturer].where(df_flights['arr_delay'] > 0)
    return(df_delay['arr_delay'].count())
    
#DF AMENDMENTS
    #concatenate date into one column
df_flights['date'] = pd.to_datetime(df_flights[['year','month','day']])

    #rename the multiple difference instances of Airbus, Canadair and Douglas, otherwise Airbus will be treated differently to Airbus Instrustrie, etc
for manu_name in ('AIRBUS','CANADAIR','DOUGLAS'):
    df_planes.loc[df_planes['manufacturer'].str.contains(manu_name), 'manufacturer'] = manu_name

    #left join the manufacturer from planes.csv
df_flights = pd.merge(df_flights, df_planes[['tailnum','manufacturer']], on='tailnum', how='left')

#WORKING OUT
    #remove duplicates from list
manu_set = list(dict.fromkeys(df_flights['manufacturer']))
    #apply appropriate functions to each unique manufacturer
manu_delay = [manu_delay_sum(x) for x in manu_set]
manu_delay_2 = [manu_delay_count(x) for x in manu_set]

    #create a table of counts for the origin and destination
city_table = df_flights.groupby(['origin','dest']).size().reset_index(name='count')

#ANSWERS
num_days = str(df_flights['date'].nunique())    #count the number of different dates to determine how many days are covered
num_cities = str(df_flights['origin'].nunique())    #count the number of different origin cities
max_delay_sum = max(manu_delay) #find highest sum of arrival delays
max_delay_sum_manu = manu_set[manu_delay.index(max_delay_sum)]  #name that manufacturer
max_delay_count = max(manu_delay_2) #find highest count of arrival delays
max_delay_count_manu = manu_set[manu_delay_2.index(max_delay_count)]    #name that manufacturer
connected_cities = city_table.loc[city_table['count'] == max(city_table['count'])]  #find the row with the highest count
city_1 = connected_cities.iloc[0,0]
city_2 = connected_cities.iloc[0,1] #take each city from that row

#OUTPUT
print(df_flights.head(15))
print("\nUser Story")

print("\nThe number of days covered by the flights table is " + num_days + ".")

print("\nThe number of departure cities covered by the flights database is " + num_cities + ".")

print("\nThe flights and planes tables are related by the tailnum column (the tail number of the plane doing the flight). The planes table provides details on the technical aspects of the plane by which the flight was undertaken.")

print("\nThe aeroplane manufacturer with the highest number of individual flight delays is " + max_delay_count_manu + ", however the manufacturer with the highest combined total length of delays is " + max_delay_sum_manu + ".")

print("\nThe two most connected cities are " + city_1 + " and " + city_2 + ".")

    #create csv files
df_flights.to_csv('flightsjoined.csv')
city_table.to_csv('connectedcities.csv')

#CLOSE OUTPUT FILE
sys.stdout.close()
