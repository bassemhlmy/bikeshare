import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = {
    '1': 'chicago',
    '2': 'new york city',
    '3': 'washington'
}
months = {
    '0': 'all',
    '1': 'january',
    '2': 'february',
    '3': 'march',
    '4': 'april',
    '5': 'may',
    '6': 'june',
}
days = {
    '0': 'all',
    '1': 'monday',
    '2': 'tuesday',
    '3': 'wednesday',
    '4': 'thursday',
    '5': 'friday',
    '6': 'saturday',
    '7': 'sunday'
}

filters = ['day', 'month', 'both', 'all']


def entry_validation(prompt_msg, validation_entry):
    """
    Validate user entry, return message if there is an entry error or user input if its correct entry
    """
    try:
        user_input = str(input(prompt_msg)).lower()

        while user_input not in validation_entry:
            print('Sorry... Wrong Entry Please Try Again !')
            user_input = str(input(prompt_msg)).lower()

        return user_input

    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US Bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    month = ''
    day = ''
    filter_type = ''
    # get user input for City selection
    prompt_msg = ('Would you like to see data for Chicago, New York, or Washington?\nEnter the city # from 1 to 3 => (1 => Chicago, 2 => New York, or 3 => Washington) : ')
    city = entry_validation(prompt_msg, cities.keys())
    # get user input for filter option (day,month or no at all (no filter))
    prompt_msg = (
        'Would you like to filter the data by month, day, both or not at all?')
    filter_type = entry_validation(prompt_msg, filters)
    # get user input for day of week (monday, tuesday, ... sunday)
    if filter_type == 'day':
        month = '0'
        prompt_msg = (
            'Please enter day# from 0 to 7 => (0 => all, Monday => 1 ... Sunday => 7 ) : ')
        day = entry_validation(prompt_msg, days.keys())
    # get user input for month (all, january, february, ... , june)
    elif filter_type == 'month':
        day = '0'
        prompt_msg = (
            'Please enter month # from 0 to 6 => (0 => all , 1 => January .... 6=> June ): ')
        month = entry_validation(prompt_msg, months.keys())
        # get user input for both (month and day) (all, january, february, ... , june)
    elif filter_type == 'both':
        prompt_msg = (
            'Please enter month # from 0 to 6 => (0 => all , 1 => January .... 6=> June ): ')
        month = entry_validation(prompt_msg, months.keys())
        prompt_msg = (
            'Please enter day# from 0 to 7 => (0 => all, Monday => 1 ... Sunday => 7 ) : ')
        day = entry_validation(prompt_msg, days.keys())

    else:
        month = '0'
        day = '0'

    print('-'*40)
    return cities[city], months[month], days[day]


def load_data(city, month, day):
    print(city.title(), month.title(), day.title())
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df = df.dropna(axis=0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['start hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may',
                  'june']
        month_num = months.index(month)+1
        df['month'] = df['Start Time'].dt.month
        df = df[df['month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
        day_num = days.index(day)
        df = df[df['day'] == day_num]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('-'*40)
    count = df['month'].value_counts().head(1).to_dict()
    print('The Most Common Month : {}'.format(count))
    # display the most common day of week
    print('-'*40)
    count = df['day'].value_counts().head(1).to_dict()
    print('The Most Common Day : {}'.format(count))
    # display the most common start hour
    print('-'*40)
    count = df['start hour'].value_counts().head(1).to_dict()
    print('The Most Common Start Hour : {}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('-'*40)
    count = df['Start Station'].value_counts().head(1).to_dict()
    print('The Most Commonly Used Start Station :')
    print(count)

    # display most commonly used end station
    print('-'*40)
    count = df['End Station'].value_counts().head(1).to_dict()
    print('The Most Commonly Used End Station :')
    print(count)
    # display most frequent combination of start station and end station trip
    count = df.groupby(['Start Station'])[
        'End Station'].value_counts().head(1).to_dict()
    print('-'*40)
    print('The most frequent combination of start station and end station trip {}'.format(
        count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('-'*40)
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = pd.Timedelta(seconds=total_travel_time)
    print('Total Travel Time : {}'.format(total_travel_time))

    # display mean travel time
    print('-'*40)
    mean_travel_time = df['Trip Duration'].mean()
    try:
        mean_travel_time = pd.Timedelta(seconds=mean_travel_time)
        print('Mean Travel Time : {}'.format(mean_travel_time))
    except:
        print('Mean Travel Time : {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    print('-'*40)
    print('Counts of User Types : {}'.format(user_types))

    if 'Gender' and 'Birth Year' in df:
        # Display counts of gender
        user_gender = df['Gender'].value_counts().to_dict()
        print('-'*40)
        print('Counts of Genders : {}'.format(user_gender))
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].value_counts().head(1).to_dict()
        print('The most earliest year : {}'.format(int(earliest_year)))
        print('The most recent year : {}'.format(int(recent_year)))
        print('The most common year : {}'.format(common_year))
    else:
        print('-'*40)
        print('"Gender" and "Birth Year" information not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Display raw data five rows at a time
    """
    while True:
        prompt_msg = (
            'would like want to see the 5 rows of individual raw trip data ?(y/n) : ')
        answer = entry_validation(prompt_msg, ['y', 'n'])
        if answer == 'y':
            for i in range(5):
                print(df.iloc[[i]])

        elif answer == 'n':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
