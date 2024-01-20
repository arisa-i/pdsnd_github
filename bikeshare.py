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
    city_chk=False
    filter_chk=False
    month_chk=False
    day_chk=False
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while city_chk==False:
        city = input("\nWould you like to see data for Chicago, New York, or Washington?\n").lower()
        if city in ('chicago','new york city','washington'):
            city_chk=True
        else:
            print('\nPlease select from Chicago, New York, or Washington.')
    
    # Get user input for filtering.
    while filter_chk==False:
        filter = input("\nWould you like to filter the data by month, day, or not at all?\n").lower()
        if filter in ('no','','not at all'):
            filter_chk=True
            month='all'
            day='All'
            print('-'*40)
            print('OK! Let\'s explore all data for {}.'.format(city.title()))
        elif filter == 'month':
            filter_chk=True
            day='All'
            # Get user input for month (all, january, february, ... , june).
            while month_chk==False:
                month = input("\nWhich month - January, February, March, April, May, or June?\n").lower()
                if month in ('january','february','march','april','may','june'):
                    month_chk=True
                else:
                    print('\nPlease check your input: ',month)
            print('-'*40)
            print('OK! Let\'s explore the data for {} in {}.'.format(city.title(),month.title()))
        elif filter == 'day':
            filter_chk=True
            month='all'
            # Get user input for day of week (all, monday, tuesday, ... sunday).
            while day_chk==False:
                day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").title()
                if day in ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'):
                    day_chk=True
                else:
                    print("\nPlease check your input: ",day)
            print('-'*40)
            print('OK! Let\'s explore the data for {} on {}.'.format(city.title(),day))
        else:
            print("\nPlease check your input: ",filter)

    
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
    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # Filter by month to create the new dataframe.
        df = df[df['month']==month]

    # Filter by day of week if applicable.
    if day != 'All':
        # Filter by day of week to create the new dataframe.
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    print("### Most common month: ", df['month'].mode()[0])

    # Display the most common day of week.
    print("### Most common day: ", df['day_of_week'].mode()[0])

    # Display the most common start hour.
    print("### Most common start hour: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    print("### Most commonly used start station: ", df['Start Station'].mode()[0])

    # Display most commonly used end station.
    print("### Most commonly used end station: ", df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip.
    df['conbination']=df['Start Station']+df['End Station']
    print("### Most frequent conbination of start station and end station trip: ", df['conbination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    print("### Total travel time: ", df['Trip Duration'].sum())

    # Display mean travel time.
    print("### Mean travel time: ", df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    print("### Counts of user type: ", df['User Type'].value_counts())

    if 'Gender' in df.columns:
        df['Gender'].fillna('N/A',inplace=True)
        # Display counts of gender.
        print("### Counts of gender: ", df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth.
        print("### Ealiest year of birth: ", int(df['Birth Year'].min()))
        print("### Most recent year of birth: ", int(df['Birth Year'].max()))
        print("### Most common year of birth: ", int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0

    while view_data== 'yes': 
        print(df.iloc[start_loc:start_loc+5]) 
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
