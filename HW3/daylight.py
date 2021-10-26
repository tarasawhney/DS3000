import requests
import json



def get_sunrise_sunset(lat, lng, date):
    """ gets sunrise / sunset raw data from
    
    https://sunrise-sunset.org/api
    
    Args:
        lat (float): lattitude
        lon (float): longitude    
        date (str): date to query, format: '2021-02-13'
        
    Returns:
        sun_dict (dict): dict of json (see clean_sun_dict())
    """
    
    # call api, store result and convert from json to dict
    url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}'
    url_text = requests.get(url).text 
    sun_dict = json.loads(url_text)
    
    # store location and date (for record keeping)
    sun_dict['lat-lng'] = lat, lng
    sun_dict['date'] = date
    
    return sun_dict
  
  # Given this test case is Boston those values might look funny at first, see Part 3 below for explanation
sun_dict = get_sunrise_sunset(lat=42.3601, lng=-71.0589, date='2021-02-13')

sun_dict_expected = \
{'results': {'sunrise': '11:41:56 AM',
  'sunset': '10:14:49 PM',
  'solar_noon': '4:58:22 PM',
  'day_length': '10:32:53',
  'civil_twilight_begin': '11:13:10 AM',
  'civil_twilight_end': '10:43:35 PM',
  'nautical_twilight_begin': '10:40:14 AM',
  'nautical_twilight_end': '11:16:31 PM',
  'astronomical_twilight_begin': '10:07:40 AM',
  'astronomical_twilight_end': '11:49:05 PM'},
 'status': 'OK',
 'lat-lng': (42.3601, -71.0589),
 'date': '2021-02-13'}

assert sun_dict == sun_dict_expected, 'get_sunrise_sunset() error'

import pytz
from datetime import datetime

def change_tz(dt, timezone_from, timezone_to):
    """ converts unix time to a datetime object
    
    Args:
        dt (datetime): datetime (or time) object without timezone
        timezone_from (str): timezone of input unix_time
        timezone_to (str): timezone of output datetime
        
    Returns:
        dt (datetime): datetime object corresponding to 
            unix_time
    """
    # add timezone to given datetime
    from_zone = pytz.timezone(timezone_from)
    dt_from = from_zone.localize(dt)

    # Convert time zone to to_zone
    to_zone = pytz.timezone(timezone_to)
    dt_to = dt_from.astimezone(to_zone)

    return dt_to
  
  import pytz

# build test case input / output
dt_no_tz = datetime(2021, 2, 13, 9, 54, 4, 270088)
dt_expect = datetime(2021, 2, 13, 14, 54, 4, 270088, tzinfo=pytz.timezone('GMT'))

# compute actual output
dt = change_tz(dt_no_tz, timezone_from='US/Eastern', timezone_to='GMT')

assert dt == dt_expect, 'change_tz() error'

# build test case input / output
dt_no_tz = datetime(2021, 2, 13, 9, 54, 4, 270088)
dt_expect = datetime(2021, 2, 13, 9, 54, 4, 270088, tzinfo=pytz.timezone('GMT'))

# compute actual output
dt = change_tz(dt_no_tz, timezone_from='GMT', timezone_to='GMT')

assert dt == dt_expect, 'change_tz() error'

from datetime import datetime

def clean_sun_dict(sun_dict, timezone_to):
    """ builds pandas series and cleans output of API
    
    Args:
        sun_dict (dict): dict of json (see ex below)
        timezone_to (str): timezone of outputs (API returns
            UCT times)
            
    Returns:
        sun_series (pd.Series): all times converted to
            time objects
    
    example sun_series:
    
    date            2021-02-13 00:00:00
    lat-lng        (36.72016, -4.42034)
    sunrise                    02:11:06
    sunrise_hr                    2.185
    sunset                     13:00:34
    sunset_hr                   13.0094
    dtype: object
    """
    sun_dict_clean = dict()
    
    # clean / store date
    date = datetime.strptime(sun_dict['date'], '%Y-%m-%d')
    sun_dict_clean['date'] = date
    
    # store lat longitude
    sun_dict_clean['lat-lng'] = sun_dict['lat-lng']
    
    # clean / store times of sunrise sunset
    for label in ['sunrise', 'sunset']:
        # build datetime object
        # we include the date given daylight's saving
        dt_str = sun_dict['date'] + ' ' + sun_dict['results'][label]
        dt = datetime.strptime(dt_str, '%Y-%m-%d %I:%M:%S %p')
        
        # convert to proper timezone & store only time
        dt = change_tz(dt, timezone_from='UCT', timezone_to=timezone_to)
        sun_dict_clean[label] = dt.time()
        
        # compute hours into day of sunrise / sunset
        label_hr = f'{label}_hr'
        sun_dict_clean[label_hr] = dt.hour + dt.minute / 60 + dt.second / 3600
        
    # cast to series
    return pd.Series(sun_dict_clean)
  
  import pandas as pd
from datetime import time

sun_dict = \
    {'results': {'sunrise': '7:07:06 AM',
      'sunset': '5:56:34 PM',
      'solar_noon': '12:31:50 PM',
      'day_length': '10:49:28',
      'civil_twilight_begin': '6:40:39 AM',
      'civil_twilight_end': '6:23:00 PM',
      'nautical_twilight_begin': '6:10:17 AM',
      'nautical_twilight_end': '6:53:22 PM',
      'astronomical_twilight_begin': '5:40:12 AM',
      'astronomical_twilight_end': '7:23:27 PM'},
     'status': 'OK',
     'lat-lng': (36.72016, -4.42034),
     'date': '2021-02-13'}

# test without timezone conversion
sun_series = clean_sun_dict(sun_dict, timezone_to='GMT')

sun_series_exp = pd.Series(
{'date': datetime(year=2021, month=2, day=13),
'lat-lng': (36.72016, -4.42034),
'sunrise': time(hour=7, minute=7, second=6),
'sunrise_hr': 7.118333333333333,
'sunset': time(hour=17, minute=56, second=34),
'sunset_hr': 17.942777777777778})

assert sun_series.eq(sun_series_exp).all(), 'clean_sun_dict() error'

# test with timezone conversion
sun_series = clean_sun_dict(sun_dict, timezone_to='US/Eastern',)

sun_series_exp = pd.Series(
{'date': datetime(year=2021, month=2, day=13),
'lat-lng': (36.72016, -4.42034),
'sunrise': time(hour=2, minute=7, second=6),
'sunrise_hr': 2.118333333333333,
'sunset': time(hour=12, minute=56, second=34),
'sunset_hr': 12.942777777777778})

assert sun_series.eq(sun_series_exp).all(), 'clean_sun_dict() error'

from datetime import timedelta

def get_annual_sun_data(loc_dict, year=2021, period_day=30): 
    """ pulls evenly spaced sunrise / sunsets from API over year per city
    
    Args:
        loc_dict (dict): keys are cities, values are tuples of 
            (lat, lon, tz_str) where tz_str is a timezone
            string included in pytz.all_timezones
        year (int): year to query
        period_day (int): how many days between data queries
            (i.e. period_day=1 will get every day for the year)
            
    Returns:
        df_annual_sun (DataFrame): each row represents a 
            sunrise / sunset datapoint, see get_sunrise_sunset()
    """
    # create date_str of API
    date = datetime(year=year, month=1, day=1)
    
    # convert period_day to a timedelta object to loop
    sample_period = timedelta(days=period_day)
    
    df_annual_sun = pd.DataFrame()
    while date.year < year + 1:
        for city, (lat, lng, timezone) in loc_dict.items():
            # get and clean data
            date_str = date.strftime('%Y-%m-%d')
            sun_dict = get_sunrise_sunset(lat, lng, date_str)
            sun_series = clean_sun_dict(sun_dict, timezone_to=timezone)

            # record city, aggregate in dataframe
            sun_series['city'] = city
            df_annual_sun = df_annual_sun.append(sun_series, ignore_index=True)
        
        # increment date
        date += sample_period
        
    return df_annual_sun
  
  loc_dict = {'Boston': (42.3601, -71.0589, 'US/Eastern'),
            'Cairo': (30.0444, 31.2357, 'Egypt'),
            'Sydney': (-33.8688, 151.2093, 'Australia/Sydney')}

# you may find that setting period_day to a larger value is quicker for debug
# period_day=5 takes about a minute or so given the API do30es 2-3 requests / sec
df_annual_sun = get_annual_sun_data(loc_dict, year=2021, period_day=30)

df_annual_sun.head()

import seaborn as sns

sns.set(font_scale=1.5)

def plot_daylight(df_annual_sun):
    """ produces a plot of daylight seen across cities
    
    Args:
        df_annual_sun (DataFrame): each row represents a 
            sunrise / sunset datapoint, see get_sunrise_sunset()
    """
    
    for city in df_annual_sun['city'].unique():
        # boolean select just rows corresponding to city
        city_bool = df_annual_sun['city'] == city
        df_city = df_annual_sun.loc[city_bool, :]

        # get sunrise, sunset and time
        top = df_city['sunrise_hr']
        btm = df_city['sunset_hr']
        x = df_city['date']

        # shade area of daylight
        plt.fill_between(x, top, btm, label=city, alpha=.2)

    # groom graph features
    plt.gcf().set_size_inches((12, 8))
    plt.ylabel('Local Military Time')
    plt.xlabel('Date')
    plt.suptitle('Daylight at each location')
    plt.legend()

# takes about a minute to run with period_day=7, worth it to characterize
# the sudden jumps due to daylight savings times
df_annual_sun = get_annual_sun_data(loc_dict, year=2021, period_day=7)

plot_daylight(df_annual_sun)
