import csv
import datetime
import requests

'''
id - person's id
name - person's name
age - person's age
morning_happiness - well-being perceived from 1-10 at the beginning of the day
night_happiness - well-being perceived from 1-10 at the end of the day
date - date as DD/MM/YYYY
weekday - week day
hours_of_sleep - hours of sleep the night before
screen_time_minutes - phone screen time
workout_minutes - minutes spent working out
outdoor_minutes - minutes spent outdoor
weather_conditions - conditions of the weather (sunny, rainy, cloudy, etc...)
temperature - average temperature
nutrition - quality of the nutrition from 1-10, with 1 - horrible and 10 - excellent
sexual_relationships - yes (1) or no (0)
number_pages_read - number of pages of a book read
social_minutes - number of minutes spent socializing with people
'''

user_names = ['rafa', 'marta']

def process_date(date_str) -> datetime.date:
    date_array = date_str.split('-')
    return datetime.date(int(date_array[2]), int(date_array[1]), int(date_array[0]))


def get_weekday(date) -> str:
    return date.strftime("%A")


# str_date in format dd-mm-yyyy
def get_weather(date) -> tuple:
    params: dict = {'key': 'c30c96eca7c6490f954140634242210', 'q': '38.736946,-9.142685',
                    'dt': date.strftime('%Y-%m-%d')}

    response = requests.get('http://api.weatherapi.com/v1/history.json', params=params)
    # print(response.json())
    forecast_day = response.json()['forecast']['forecastday'][0]['day']
    # print(f"Average temperature is = {forecast_day['avgtemp_c']} and weather is {forecast_day['condition']['text']}")
    avg_temp: float = forecast_day['avgtemp_c']
    weather_condition: str = forecast_day['condition']['text']
    return avg_temp, weather_condition


def get_input() -> tuple:
    input_type: int = int(input('type of input: 1-short and 2-long: '))

    if input_type == 2:
        params = input(
            'name, date, morning_well_being (1-very bad mood, 10-excellent mood), \n'
            'night_well_being (1-very bad mood, 10-excellent mood), hours_of_sleep, screen_time (minutes), \n'
            'workout_minutes, outdoor_minutes, nutrition (1-horrible, 10-excellent), sexual_relationships (y/n), \n'
            'number_of_pages_read, social_minutes: \n').split()

        name = params[0]
        date_str = params[1]
        morning_well_being = int(params[2])
        night_well_being = int(params[3])
        hours_of_sleep = float(params[4])
        screen_time_minutes = int(params[5])
        workout_minutes = int(params[6])
        outdoor_minutes = int(params[7])
        nutrition = int(params[8])
        sexual_relationships = params[9]
        number_of_pages_read = int(params[10])
        social_minutes = int(params[11])

    else:
        name = input('name: ')
        while name not in user_names:
            print("Unauthorized User, please try again.")
            name = input('name: ')
        date_str = input('date: ')
        morning_well_being = int(input('morning_well_being (1-very bad mood, 10-excellent mood): '))
        night_well_being = int(input('night_well_being (1-very bad mood, 10-excellent mood): '))
        hours_of_sleep = float(input('hours of sleep: '))
        screen_time_minutes = int(input('screen_time (minutes): '))
        workout_minutes = int(input('workout_minutes: '))
        outdoor_minutes = int(input('outdoor_minutes: '))
        nutrition = int(input('nutrition (1-horrible, 10-excellent): '))
        sexual_relationships = input('sexual_relationships (y/n): ')
        number_of_pages_read = int(input('number_of_pages_read: '))
        social_minutes = int(input('social_minutes: '))




    return name, date_str, morning_well_being, night_well_being, hours_of_sleep, screen_time_minutes, workout_minutes, \
        outdoor_minutes, nutrition, sexual_relationships, number_of_pages_read, social_minutes

def process_params(name, date_str, sexual_relationships) -> tuple:
    if date_str == 't':
        date = datetime.datetime.today().date()
    else:
        date = process_date(date_str)

    # Get weather and temperature
    weather_info = get_weather(date)
    avg_temp = weather_info[0]
    weather_condition = weather_info[1]

    # Code yes or no
    if sexual_relationships == 'y':
        sexual_relationships_coded = 1
    elif sexual_relationships == 'n':
        sexual_relationships_coded = 0
    else:
        raise Exception("y or n")

    # Get id and age by name
    if name == 'rafa':
        id = 0
        age = 23
    elif name == 'marta':
        id = 1
        age = 23
    else:
        raise Exception('unknown user')

    # Get weekday from date
    weekday = get_weekday(date)

    return avg_temp, weather_condition, sexual_relationships_coded, id, age, weekday, date

name, date_str, morning_well_being, night_well_being, hours_of_sleep, screen_time_minutes, workout_minutes, \
        outdoor_minutes, nutrition, sexual_relationships, number_of_pages_read, social_minutes = get_input()

avg_temp, weather_condition, sexual_relationships_coded, id, age, weekday, date = \
    process_params(name, date_str, sexual_relationships)

column_names = ['id', 'name', 'age', 'morning_well_being', 'night_well_being', 'date', 'weekday', 'hours_of_sleep',
                'screen_time_minutes', 'workout_minutes', 'outdoor_minutes', 'weather_conditions', 'temperature',
                'nutrition', 'sexual_relationships', 'number_pages_read', 'social_minutes']

# Open a CSV file in write mode
with open('C:\\Users\\Marta Costa\\PycharmProjects\\HappinessTracker\\happiness_tracker.csv', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=',')

    new_row = [id, name, age, morning_well_being, night_well_being, date, weekday, hours_of_sleep, screen_time_minutes,
               workout_minutes, outdoor_minutes,
               weather_condition, avg_temp, nutrition, sexual_relationships_coded, number_of_pages_read,
               social_minutes]

    # Write a single line to the CSV file
    writer.writerow(new_row)
