import pandas as pd

bike_id = ['037', '379', '398', '37B', 'BRG']
bike_dict = {'Bike ID': ['037', '379', '398', '37B', 'BRG'],
            'Rider ID': [3, 1, 7, 3, 7],
             'Make': ['Bianchi', 'Duratec', 'Trek', 'Trek', 'Canondale'],
             'Color': ['Celeste', '<no paint>', 'Red', 'Black', 'Black'],
             'Bike Type': ['Road', 'Cyclocross', 'Road', 'Mountain', 'Mountain'],
             'Weight (g)': [8200, 9500, 9000, 13607, 15005],
             'Time Trial 1 (s)': [450, 510, 432, 561, 524],
             'Time Trial 2 (s)': [205, 222, 211, 301, 299]}

df_bike_race = pd.DataFrame(bike_dict, index=bike_id)

df_bike_race.to_csv('bike_race.csv')
df_bike_race

# get maximum weight across all rows of bikes
max_weight = df_bike_race['Weight (g)'].max()

# produce dataframe containing only this bike
df_bike_race.loc[df_bike_race['Weight (g)'] == max_weight, :]

# fancy one liner (not needed for full credit)
# get index of bike which has maximum weight across all rows of bikes
df_bike_race['Weight (g)'].idxmax()

# compute mean time trial
df_bike_race['Time Trial Mean'] = (df_bike_race['Time Trial 1 (s)'] + 
                                   df_bike_race['Time Trial 2 (s)']) / 2

# get minimum average race time
min_time_trial_mean = df_bike_race['Time Trial Mean'].min()
print(min_time_trial_mean)

# produce dataframe containing only this bike
df_bike_race.loc[df_bike_race['Time Trial Mean'] == min_time_trial_mean, :]

# fancy (replaces two lines directly above)
df_bike_race['Time Trial Mean'].idxmin()

# get list of all unique bike types
bike_type_list = list(df_bike_race['Bike Type'].unique())


# compute mean weight per bike type
bike_type_weight_dict = dict()
for bike_type in bike_type_list:
    series_type = df_bike_race['Bike Type'] == bike_type
    df = df_bike_race.loc[series_type, :]
    bike_type_weight_dict[bike_type] = df['Weight (g)'].mean()
    
print(bike_type_weight_dict)

# one-liner solution
df_bike_race.groupby('Bike Type')['Weight (g)'].mean()
