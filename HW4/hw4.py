#Part 1.1
def get_url(url):
    """ gets html associated with a url 
    
    Args:
        url (str): url website to look up
        
    Returns:
        html_str (str): html associated with this url
    """
    pass
  
#Part 1.2
def clean_pitchfork(html_str):
    """ scrapes artists / track from a pitchfork page
    
    ex:
    https://pitchfork.com/reviews/best/tracks/?page=1
    
    Args:
        html_str (str): html of pitchfork page
        
    Returns:
        df_pitch (DataFrame): each row is a song.  
            contains columns 'artist', 'track'  
    """
    pass
  
#Part 1.3
def get_popularity(df_track, api_key):
    """ queries spotify API for popularity of all songs in df_track
    
    Args:
        df_track (DataFrame): a dataframe which contains (at least)
            columns: artist & track.  one row per song
        api_key (str): api key of spotify API
        
    Returns:
        df_track (DataFrame): each row is a song.  
            contains columns 'artist', 'track' and 
            `popularity` as well as other columns in
            the input df_track.  note: this is a copy
            of the input (doesn't overwrite)
    """
    pass
  
#Part 1.4
def hist_feat(df, feat):
    """ produces a histogram of feat per unique source
    
    Args:
        df (DataFrame): contains a column source
        feat (str): some other column of input df
    """
    pass
  
#Part 2
import requests

def get_url(url):
    """ gets html associated with a url 
    
    Args:
        url (str): url website to look up
        
    Returns:
        html_str (str): html associated with this url
    """
    return requests.get(url).text
  
url='https://www.billboard.com/articles/news/list/9494940/best-songs-2020-top-100/'
get_url(url)

#Part 3
from bs4 import BeautifulSoup
import pandas as pd

def clean_pitchfork(html_str):
    """ scraps artists / track from a pitchfork page
    
    ex:
    https://pitchfork.com/reviews/best/tracks/?page=1
    
    Args:
        html_str (str): html of pitchfork page
        
    Returns:
        df_pitch (DataFrame): each row is a song.  
            contains columns 'artist', 'track' and 
            'source' (source is always 'pitchfork')    
    """
    # build soup
    soup = BeautifulSoup(html_str)
    
    df_pitch = pd.DataFrame()
    for song in soup.find_all('div', class_='track-collection-item'):
        # extract artist
        artist = song.find_all('ul', class_='artist-list')[0].text
        
        #extract track
        track = song.find_all('h2', class_='track-collection-item__title')[0].text
        
        # discard all directional double quotes
        track = track.replace('“', '')
        track = track.replace('”', '')
        
        # collect song data in dataframe
        song_dict = {'artist': artist, 
                     'track': track,
                     'source': 'pitchfork'}
        df_pitch = df_pitch.append(song_dict, ignore_index=True)
        
    return df_pitch
url = 'https://pitchfork.com/reviews/best/tracks/?page=1'
html_str = get_url(url)
df_pitch1 = clean_pitchfork(html_str)
df_pitch1.head()

#Part 4 
max_page = 10

df_pitch = pd.DataFrame()
for page_idx in range(1, max_page + 1):
    # build url of a given page of pitchfork music
    url = f'https://pitchfork.com/reviews/best/tracks/?page={page_idx}'
    
    # get pitchfork page
    html_str = get_url(url)
    
    # process to dataframe
    df_pitch_page = clean_pitchfork(html_str)
    
    # collect each page in one common dataframe: df_pitch
    df_pitch = df_pitch.append(df_pitch_page, ignore_index=True)

# output shape to jupyter notebook (56 songs total when I ran this Feb 25)
df_pitch.shape

#Part 5 
url = 'https://www.brainyquote.com/topics/websites-quotes'
html_str = get_url(url)

def clean_quote(html_str):
    """ cleans brainy quote quotes
    
    ex: https://www.brainyquote.com/topics/websites-quotes
    
    Args:
        html_str (str): html of website
        
    Returns:
        df_quote (pd.DataFrame): contains columns author,
            text and a unique column for every tag (e.g.
            Communication, Family, Positive, Love...).
            values of a tag column are 1 where tag 
            applies to the row's quote, otherwise they're 0
    """
    # build soup from html_str
    soup = BeautifulSoup(html_str)

    df_quote = pd.DataFrame()

    for quote in soup.find_all('div', class_='m-brick'):
        # get author and text
        a_list = quote.find_all('a')
        author = a_list[1].text
        text = a_list[0].text

        quote_dict = {'author': author,
                      'text': text}

        # ex credit: get tags too
        for tag in quote.find_all('a', class_='oncl_klc'):
            quote_dict[tag.text] = 1

        # add quote to dataframe
        df_quote = df_quote.append(quote_dict, ignore_index=True)

    # ex credit: all NaNs are where tag wasn't observed, map them to 0
    df_quote = df_quote.fillna(0)
    return df_quote
max_page = 3

df_quote = pd.DataFrame()
for idx in range(1, max_page + 1):
    # get dataframe from page idx
    url = f'https://www.brainyquote.com/topics/websites-quotes_{idx}'
    html_str = get_url(url)
    df_quote_idx = clean_quote(html_str)
    
    # aggregate in one dataframe
    df_quote = df_quote.append(df_quote_idx, ignore_index=True)
df_quote_tag = df_quote.copy()

del df_quote_tag['author']
del df_quote_tag['text']

# sum the number of quotes with each tag
tag_count = df_quote_tag.sum(axis=0)

# sort according to which tag is most common first
tag_count = tag_count.sort_values(ascending=False)

# pandas will use ... if too many rows, setting this option
# ensures we can read up to 500 rows before it uses the ...
pd.set_option('display.max_rows', 500)

# print them out so we can see
tag_count
