import seaborn as sns

# https://www.kaggle.com/shivam2503/diamonds
# (this kaggle data is same as seaborn)
df_diamonds = sns.load_dataset('diamonds')
df_diamonds.head()

#Part 1 
import matplotlib.pyplot as plt
import pandas as pd
    
df_all = pd.DataFrame()
for cut in ('Ideal', 'Good', 'Fair'):
    # boolean index to only rows with a given cut
    cut_bool = df_diamonds['cut'] == cut
    df_diamonds_cut = df_diamonds.loc[cut_bool, :]
    
    # take mean by carat
    df_diamonds_carat = df_diamonds_cut.groupby('carat').mean()
    df_diamonds_carat['cut'] = cut
    
    # appending multiple rows to df
    df_all = df_all.append(df_diamonds_carat)
    
import plotly.express as px

df_all = df_all.reset_index()
fig = px.scatter(data_frame=df_all, x='carat', y='price', color='cut')
fig.show()
fig.write_html('mass_vs_price.html')
