# Importing required libraries
import time
import pandas as pd
import datetime

# City data dictionary
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Days in chronological order
days_dict = {'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday',
             'sat': 'Saturday', 'sun': 'Sunday', 'all': 'No filters'}

# Months in chronological order
month_dict = {'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April', 'may': 'May', 'jun': 'June',
              'all': 'No filters'}


# Function to confirm a user's input
def confirm_input():
    while True:
        answer = str(input("Please confirm your input\nEnter 'y' to continue or 'n' to restart:\n").strip().lower())
        if answer not in ("y", "n"):
            print("\nInvalid Response. Please try again")
            continue
        elif answer == "y":
            break
        else:
            get_filters()


# Function to filter data by user's input
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print()
    print('-' * 44)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-' * 44)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print()
    while True:
        city = (input("Which city do you want to select bikeshare data from?\nPlease enter either 'Chicago', "
                      "'New York City' or 'Washington'\n")).strip().lower()
        if city in ["chicago", "new york city", "washington"]:
            break
        else:
            print("\nInvalid input!!! Trying again...")

    # get user input for month (all, january, february, ... , june)
    print()
    while True:
        month = (input("From January to June, which Month do you want to filter the bikeshare data by?\nPlease enter "
                       "'Jan', 'Feb', 'Mar', 'Apr', 'May' or 'Jun' to represent each of the months.\nEnter 'all' "
                       "to apply no month filter\n")).strip().lower()
        if month in ["jan", "feb", "mar", "apr", "may", "jun", "all"]:
            break
        else:
            print("\nInvalid input!!! Trying again")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print()
    while True:
        day = (input("What day of the week do you want to filter the bikeshare data by?\nPlease enter 'Mon', 'Tue', "
                     "'Wed', 'Thu', 'Fri', 'Sat' or 'Sun' to represent the day of the week.\nEnter 'all' to apply no "
                     "day filter\n")).strip().lower()
        if day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun", "all"]:
            break
        else:
            print("\nInvalid input!!! Trying again...")

    print("\nYour inputs are..\n\tCity : {}\n\tMonth : {}\n\tDay : {}\n"
          "".format(city.capitalize(), month_dict[month], days_dict[day]))
    confirm_input()

    print('-' * 48)
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

    # loading city data file into a data frame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract Month from the Start Time column to create month column
    df['Month'] = df['Start Time'].dt.month

    # extract day of week from the Start Time column to create day of week column
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create hour column
    df['Hour'] = df['Start Time'].dt.hour

    # Filtering by month if user enters a month other than 'all'
    if month != 'all':
        # Listing months in chronological order
        months = ["jan", "feb", "mar", "apr", "may", "jun"]

        # Month converted to numbers
        month = months.index(month) + 1

        # Filtering by month to create new data frame
        df = df[df['Month'] == month]

    # Filtering by month if user enters a day other than 'all'
    if day != 'all':
        # filter by day of week to create the new data frame
        df = df[df['Day_of_Week'] == days_dict[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    month_int_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    print('\t1. Most Common Month:', month_int_dict[popular_month])

    # display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print('\t2. Most Common Day of Week:', popular_day)

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('\t3. Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\t1. Most commonly used start station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\t2. Most commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    start_end_comb = df['Start-End Combination'].mode()[0]
    print('\t3. Most frequent combination of start station and end station trip:', str(start_end_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_travel_time = df['Trip Duration'].sum()

    # support type for timedelta seconds component
    total_travel_time = sum_travel_time.astype('float64', copy=False)

    # convert time to timedelta object
    converted_time = datetime.timedelta(seconds=total_travel_time)

    # display total travel time in time delta format
    print('\t1. Total travel time is as follows: \n\t\tin seconds ==> {} seconds\n\t\tin time delta format ==> {}'.
          format(str(total_travel_time), str(converted_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # convert time to timedelta object
    mean_converted_time = datetime.timedelta(seconds=mean_travel_time)
    print('\n\t2. Mean travel time is as follows: \n\t\tin seconds ==> {} seconds\n\t\tin time delta format ==> {}'.
          format(str(mean_travel_time), str(mean_converted_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df["User Type"].value_counts().to_string()
    # Splitting the user types data into array for desired output format
    user_type_array = user_type_count.split()
    print("\t1. Counts of users' type is as follows:\n\t\t\t{} : {} counts\n\t\t\t{} : {} "
          "counts".format(user_type_array[0], user_type_array[1], user_type_array[2], user_type_array[3]))

    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts().to_string()
        # Splitting the users' gender data into array for desired output format
        user_gender_array = gender_count.split()

        # Counting null values in Gender
        nan_total = df["Gender"].isna().sum()

        print("\n\t2.Counts of users' gender is as follows:\n\t\t\t{} : {} counts\n\t\t\t{} : {} counts\n\t\tNote: "
              "there were {} NaN data values in the 'Gender' column".format(user_gender_array[0], user_gender_array[1],
                                                                            user_gender_array[2], user_gender_array[3],
                                                                            nan_total))
    else:
        print("\n\t2. {} has no data for users' gender".format((str(city)).capitalize()))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\n\t3. Earliest year of birth:', int(earliest_year))
        print('\t4. Most recent year of birth:', int(most_recent_year))
        print('\t5. Most common year of birth:', int(most_common_year))

    else:
        print("\t3. {} has no data for users' year of birth".format((str(city)).capitalize()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    response = input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").lower()
    # Catch if a user enters just 'y' as earlier used in code
    if response in ("yes", "y"):
        i = 0

        while True:
            # Printing from lower limit to length of dataframe rows if 'i' is out of bounds
            if i + 5 > len(df.index) - 1:
                print(df.iloc[i:len(df.index), :])
                print("You've reached the end of the rows")
                break

            # Printing the dataframe in a set of 5 rows if 'i' is not out of bounds
            print(df.iloc[i:i + 5, :])
            i += 5

            # Asking to show more rows in 5
            response_show_next_five = input("\nWould you like to see the next 5 rows? Enter 'yes' or "
                                            "'no'\n").strip().lower()
            # Catch if a user enters just 'y' as earlier used in code
            if response_show_next_five not in ("yes", "y"):
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)
        #
        restart = input("\nWould you like to restart? Enter 'y' to restart or any other character "
                        "to exit the program.\n")
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
    main()
