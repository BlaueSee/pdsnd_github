import time
import pandas as pd
import numpy as np
from time import sleep

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # Get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nYou wanna see the data for which city? Please choose from Chicago, New York or Washington: ').lower()
    while city not in CITY_DATA.keys():
        print('Wrong way there! Please choose again!')
        city = input('\nPlease choose from Chicago, New York or Washington: ').lower()

    # Get user input for month (all, january, february, ... , june)
    print(f"\nOK, {city.title()} then.")
    sleep(1)
    MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all months']
    month = input("\nWhich month(s) do you want to seek the data from?\nNote that, you can only choose from January to June, and the input is not case sensitive (e.g. june or JUNE are both fine).\n(You can also view the data for all months from January to June by typing 'all months'!)\n").lower()
    while month not in MONTH_DATA:
        print("\nThat won't do! Please try again with a month from January to June, or all months with 'all months'.")
        month = input().lower()
    
    print(f"\nAll right, {month.title()} it is!")
    sleep(1)    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_LIST = ['all days', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("\nWhich day(s) of the week do you want to seek the data from?\nYou can choose from Monday to Sunday, and the input is not case sensitive (e.g. sunday or SUNDAY are both fine).\n(You can also view the data for all days in a week from Monday to Sunday by typing 'all days'!)\n").lower()
    while day not in DAY_LIST:
        print("\nThat won't do! Please try again with a day from Monday to Sunday, or all days with 'all days'.")
        day = input().lower()
    
    print(f"\nThat's good! {day.title()} will do!")
    sleep(1)
    print(f"\nThank you for choosing! Here's your data for {city.title()} in {month.title()} on {day.title()}")
    print('-'*80)
    return city, month, day
    sleep(1)

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
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all months':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all days':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f"\nMost Popular Day: {popular_day}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"\nMost Popular Start Hour: {popular_hour}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]
    print(f"\nThe most frequent combination of trips are from {combo}.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # Display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('\nTotal travel time is: ', total_travel_time/3600, "hours")

    # Display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time is: ', average_travel_time/3600, "hours")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if city in ['chicago', 'new york']:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is:", earliest)
        print("\nMost recent year of birth is:", most_recent)
        print("\nThe most common year of birth is:", most_common)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
    
def display_data(df):
    """
	Displays 5 rows of data from the csv file for the selected city.
    """
    while True:
        view_df = input('\nDo you wish to view data within 5 rows of a trip? Enter yes or no\n').lower()
        if view_df.lower() == 'yes':
            print('\nPlease stretch the width of your window to accomodate all columns in one horizontal row\n')
            break
        elif view_df.lower() == 'no':
            return
        else:
            print("\nPlease try again with yes or no.")
            
    position = 0
    while view_df == 'yes' and position <= (len(df.index)-5):
        try:
            print(df.iloc[position : position + 5])
            position += 5
            view_df = input("\nDo you want to view more data?: ").lower()
        except:
            print("\nPlease try again with yes or no.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        sleep(0.5)
        time_stats(df)
        sleep(1.5)
        station_stats(df)
        sleep(1.5)
        trip_duration_stats(df)
        sleep(1.5)
        user_stats(df, city)
        sleep(0.5)

        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
