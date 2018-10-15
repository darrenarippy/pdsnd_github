import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']

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
    prompt = "Would you like to explore Chicago, New York City,"
    prompt += " or Washington data?: "
    reprompt = "Enter Chicago, New York City, or Washington: "
    city = get_filter(prompt, reprompt, list(CITY_DATA.keys()))

    # get user input for month (all, january, february, ... , june)
    prompt = "Enter a month to filter by month or 'all' for no filter: "
    reprompt = "Enter a valid month filter: "
    month = get_filter(prompt, reprompt, MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = "Enter a day to filter by day or 'all' for no filter: "
    reprompt = "Enter a valid day filter: "
    day = get_filter(prompt, reprompt, DAYS)

    print('-'*40)
    return city, month, day

def get_filter(prompt, reprompt, valid_vals):
    """
    Asks the user to specify a value for filter.

    Args:
        (str) prompt - initial prompt to present to user
        (str) reprompt - prompt to display after invalid input
        (list) valid_vals - set of valid values for user input
    Returns:
        (str) response - User response to prompt.
    """
    response = input(prompt).lower()
    while (response not in valid_vals):
        response = input(reprompt).lower()

    return response

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def peek_data(df):
    """
    Presents the raw data in df 5 rows at a time until the user indicates
    otherwise.

    Args:
        (Pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
    """
    peek = input("Would you like to view 5 rows of data?: ")
    if peek.lower() == "yes":
        print(df.head())

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (Pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    prompt = "The most common {} for bikeshare usage is {}"

    # display the most common month
    month_mode = MONTHS[(df['month'].mode()[0])].title()
    print(prompt.format("month", month_mode))

    # display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print(prompt.format("day", day_mode))

    # display the most common start hour
    hour_mode = df['Start Time'].dt.hour.mode()[0]
    hour = convert_to_12_hour(hour_mode)
    print(prompt.format("start hour", hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_to_12_hour(hour_24):
    """
    Converts an hour in 24-hour to 12-hour format, with correct AM or PM
    designation.

    Args:
        (int) hour_24 - an integer between 0 and 23
    Returns:
        (str) hour - A string in the format "<hour> <AM | PM>"
    """
    if hour_24 > 11:
        hour_24 -= 12
        hour = str(hour_24) + " PM"
    elif hour_24 == 0:
        hour_24 = 12
        hour = str(hour_24) + " AM"
    else:
        hour = str(hour_24) + " AM"

    return hour

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (Pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    prompt = "The most commonly used {} station is {}"

    # display most commonly used start station
    station_mode = df['Start Station'].mode()[0]
    print(prompt.format('start', station_mode))

    # display most commonly used end station
    station_mode = df['End Station'].mode()[0]
    print(prompt.format('end', station_mode))

    # display most frequent combination of start station and end station trip
    df_grouped = df.groupby(['Start Station', 'End Station'])[['Start Station', 'End Station']]
    freq_trip = df_grouped.size().nlargest(1)
    prompt = "The most frequent trip is from {} to {}"
    print(prompt.format(freq_trip.index[0][0], freq_trip.index[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = get_total_travel(df)
    prompt = "Users used the bikeshare"
    prompt += " system for a total of {:,} hours and {} minutes."
    print(prompt.format(total_travel[0], total_travel[1]))

    # display mean travel time
    mean_travel = get_mean_travel(df)
    prompt = "The average trip lasted {} minutes."
    print(prompt.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_total_travel(df):
    """
    Calculates the total travel time in hours and minutes for all trips in df.

    Args:
        (pandas DataFrame) df - a Pandas DataFrame containing bikeshare data.
    Returns:
        (int, int) travel_time - Total travel time in hours and minutes. minutes
        is rounded before converting to hours.
    """
    sum_duration = df['Trip Duration'].sum()
    sum_duration = sum_duration.round()
    hours = int(sum_duration // 3600)
    minutes = int(sum_duration % 60)

    return (hours, minutes)

def get_mean_travel(df):
    """
    Calculates the mean travel time in minutes for all trips in df.

    Args:
        (pandas DataFrame) df - a Pandas DataFrame containing bikeshare data.
    Returns:
        (int) mean_travel - Mean travel time in minutes. minutes
        is rounded.
    """
    mean_duration = df['Trip Duration'].mean()
    minutes = int((mean_duration / 60).round())

    return minutes

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        (Pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
        (str) city - One of Chicago, New York City, or Washington.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_by_type = count_users_by_cat(df, 'User Type')
    for key, val in counts_by_type.items():
        key = key.lower() + 's'
        prompt = "There were {:,} {}.".format(val, key)
        print(prompt)
    print()

    # Display counts of gender
    if city.title() != 'Washington':
        counts_by_gender = count_users_by_cat(df, 'Gender')
        for key, val in counts_by_gender.items():
            prompt = "There were {:,} {} users.".format(val, key)
            print(prompt)
    else:
        print("Washington dataset does not contain data on gender.")
    print()

    # Display earliest, most recent, and most common year of birth
    if city.title() != 'Washington':
        earliest, recent, common = get_birth_year_stats(df)
        prompt = "The earliest birth year is {:d}\n"
        prompt += "The most recent birth year is {:d}.\n"
        prompt += "The most common birth year is {:d}."
        print(prompt.format(earliest, recent, common))
    else:
        print("Washington dataset does not contain data on birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def count_users_by_cat(df, category):
    """
    Counts bikeshare users by type of customer.

    Arg:
        (pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
        (str) category - The category by which to group counts of users.
    Returns:
        (dict) user_counts - A dictionary of users by category (keys) and their
        associated counts (vals).
    """
    user_types = df[category].value_counts()
    user_counts = {}
    for type in user_types.index.values:
        user_counts[type] = user_types[type]

    return user_counts

def get_birth_year_stats(df):
    """
    Returns the earliest, most recent, and most common birth years among users.

    Args:
        (pandas DataFrame) df - A Pandas DataFrame containing bikeshare data.
    Returns:
        (int, int, int) year_stats - A tuple containing the birth years of
        interest. The order is earliest, recent, common.
    """
    earliest = df['Birth Year'].min()
    recent = df['Birth Year'].max()
    common = df['Birth Year'].mode()

    return (int(earliest), int(recent), int(common))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.shape[0] != 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            peek_data(df)
        else:
            print("The filters resulted in an empty dataset.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
