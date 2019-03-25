
# coding: utf-8

# In[4]:


import time, calendar
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
    while city not in CITY_DATA:
        print('please select a city from Chicago, New York City or Washington\n')
        city = input().lower()
        
    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Which month? all, January, February, March, April, May, June\n').lower()
    while month not in months:
        print('please select a month between January to June or choose "all"\n')
        month = input().lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', '1','2','3','4','5','6','7']
    day = input('Which day? Please type your response as an integer (e.g., 1=Monday) or choose "all"\n').lower()
    while day not in days:
        print('please select a day between Monday to Sunday as an integer (1,2,3 .. 7)\n')
        day = input().lower()
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read city file
    df = pd.read_csv(CITY_DATA.get(city))
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #filter by month
    df['Month'] = df['Start Time'].dt.month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]
        
    #filter by day
    df['Day'] = df['Start Time'].dt.weekday
    if day != 'all':
        day = int(day) - 1
        df = df[df['Day'] == day]
        
    df['Day Name'] = df['Start Time'].dt.weekday_name
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['Month'].nunique() > 1:
        popular_month = calendar.month_name[df['Month'].mode()[0]]
        print('The most popular month: {}'.format(popular_month))

    # display the most common day of week
    if df['Day'].nunique() > 1:
        popular_day = calendar.day_name[df['Day'].mode()[0]]
        print('The most popular day: {}'.format(popular_day))
        
    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('The most popular hour: {}'.format(popular_hour))    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most popular start station: {}'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most popular end station: {}'.format(popular_end))

    # display most frequent combination of start station and end station trip
    popular_trip = (df['Start Station']+' & '+df['End Station']).mode()[0]
    print('The most popular trip: {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_days = total_duration//86400
    total_hours = (total_duration - total_days*86400)//3600
    total_minutes = (total_duration - total_days*86400 - total_hours*3600)//60
    total_seconds = total_duration%60
    print('The total travel time is {} days, {} hours, {} minutes and {} seconds'.format(total_days, total_hours, total_minutes, total_seconds))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_days = mean_travel//86400
    mean_hours = (mean_travel - mean_days*86400)//3600
    mean_minutes = (mean_travel - mean_days*86400 - mean_hours*3600)//60
    mean_seconds = round(mean_travel%60,2)
    print('The mean travel time is {} days, {} hours, {} minutes and {} seconds'.format(mean_days, mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    print('User Type Breakdown')
    print(user_types)
    

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts().to_dict()
        print('\nGender Breakdown')
        print(gender_types)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBirth Year Breaddown')
        print('Earliest birth year: {}'.format(int(df['Birth Year'].min())))
        print('Most recent birth year: {}'.format(int(df['Birth Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_raw_data(df, city):
    """Ask user whether to see the individual data, display 5 rows each time then re-prompts the user"""
    ans = input('Would you like to see individual trip data? Type "yes" or "no"\n').lower()
    i=0
    while ans not in ('yes', 'no'):
        ans = input('please enter either yes or no\n').lower()
    while ans == 'yes':
        if city == 'washington':
            print(df.iloc[i:i+5,:7])
        else:
            print(df.iloc[i:i+5,:9])
        i+=5
        ans = input('\nWould you like to see more individual trip data? Enter yes or no\n').lower()
        while ans not in ('yes', 'no'):
            ans = input('please enter either yes or no\n').lower()
        if ans == 'no':
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        show_raw_data(df, city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

