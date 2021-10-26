# read in csv
f = './imdb_data/IMDb_movies_clean.csv'
df_movie = pd.read_csv(f)

feature = 'duration'
genre_list = ['Drama', 'Comedy', 'Horror']

bins = np.linspace(60, 170, 20)

for idx, genre in enumerate(genre_list):
    # select only movies of the given genre
    bool_genre = df_movie['genre'] == genre
    df_movie_genre = df_movie.loc[bool_genre, :]
    #df_genre = df_movie.loc[df_movie['genre'].str.contains(genre), :] # bonus point
    
    # plot
    plt.subplot(3, 1, idx + 1)
    plt.hist(df_movie_genre[feature], 
             density=True, 
             bins=bins)
    
    plt.ylabel('count')
    plt.gca().set_title(genre)
    plt.ylim(0, .05)
    
# add 'height' space between subplots
plt.subplots_adjust(hspace=.3)
    
plt.xlabel('duration (min)')
plt.gcf().set_size_inches((8, 10))
plt.suptitle('Movie duration across genres')    

for genre in ['Drama', 'Comedy']:
    df_movie_genre = df_movie.loc[df_movie['genre']==genre, :]
    
    plt.scatter(df_movie_genre['budget'], df_movie_genre['avg_vote'], 
        alpha=.4, label=genre)
plt.xscale('log')
plt.xlabel('Budget')
plt.ylabel('Avg. vote')
plt.legend()

plt.title('Budget and reception across genres')

features = ['budget', 'avg_vote']
for idx, feature in enumerate(features):
    # compute mean feature per year
    mean_feat_per_year = df_movie.groupby('year')[feature].mean()
    
    # plot
    plt.subplot(2, 1, idx + 1)
    plt.plot(mean_feat_per_year, lw=2)
    
    # bonus: shade middle 50% of data
    x = df_movie.groupby('year')[feature].describe().index
    y1 = df_movie.groupby('year')[feature].describe()['25%']
    y2 = df_movie.groupby('year')[feature].describe()['75%']
    plt.fill_between(x, y1, y2, alpha=0.5)
    
    plt.xlabel('Year')
    plt.ylabel(feature)

plt.gcf().set_size_inches(5, 10)

plt.suptitle('Are movies getting\nmore expensive and worse over time?')
