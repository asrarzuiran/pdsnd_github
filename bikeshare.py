import time
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York city, or Washington?").strip().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("\nInvalid answer. Please choose from Chicago, New York City, or Washington.")
    
    
    while True:
        filter_choice = input("\nWould you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter. ").strip().lower()
        if filter_choice in ['month', 'day', 'both', 'none']:
            break
        else:
            print("\nInvalid answer. Please choose from 'month', 'day', 'both', or 'none'.")

    
    month = 'all'
    day = 'all'

    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_choice == 'month' or filter_choice == 'both':
        while True:
            month = input("\nWhich month? January, February, March, April, May, June or all? Please type out the full month name. ").strip().lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                print("\nInvalid answer. Please choose from January, February, March, April, May, June, or 'all'.")
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_choice == 'day' or filter_choice == 'both':
        while True:
            day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? Please type out the full day name. ").strip().lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                break
            else:
                print("\nInvalid answer. Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 'all'.")

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['Start Time'].dt.month_name().str.lower() == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:', popular_month)
    # TO DO: display the most common day of week
    popular_day = df['day'].mode()[0]
    print('Most Popular day:', popular_day)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start station and end station trip:', most_frequent)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types:\n', user_types)
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Gender counts:\n', gender)
    else:
        print("no Gender data to share for this city")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        print('Earliest birth year:', earliest_birth)
        most_recent_birth = int(df['Birth Year'].max())
        print('Most recent birth year:' , most_recent_birth)
        common_birth = int(df['Birth Year'].mode()[0])
        print('Most common birth year:', common_birth)
    else:
        print("no Birth year data to share for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    index = 0
    show_data = input("\nWould you like to view individual trip data? Type 'yes' or 'no': ").strip().lower()
    while show_data == 'yes':
        if index + 5 > len(df):
            print("\nNo more data to display.")
            break    
        for i in range(index, index + 5):
            row_data = df.iloc[i].to_dict()
            print(row_data)      
        index += 5
        show_data = input("\nWould you like to view more trip data? Type 'yes' or 'no': ").strip().lower()
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()