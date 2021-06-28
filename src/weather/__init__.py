# Author: Patan Musthakheem
# Version: 1.6
# License: Apache 2.0
# fetch_weather Takes City As param And Returns It Weather data in dictionary form
# fetch_multiple_city_weather takes a list of city as param and returns a table containing City name, Temperature, Humidity, Pressure, Description
import requests, sys, time, os

kelvin = 'kelvin'
celsius = 'celsius'
fahrenheit = 'fahrenheit'

class Weather:
    def __init__(self, temperature_unit=None):
        """
        Constructor
        :param temperature_unit: celsius, fahrenheit and kelvin are only valid params
        """
        self.unit = temperature_unit
        self._avialable_units = [None, 'celsius', 'fahrenheit', 'kelvin']
        if self.unit is not None:
            if self.unit not in self._avialable_units:
                pass

    def fetch_weather(self, city, only_temp=False):
        """
        Takes City And Returns A Dictionary Containing City name, Temperature, Humidity, Pressure, Description
        :param city: City Name
        :param only_temp: if true return only that unit of temperature else return all units of temperatures
        :return: Dictionary containing  City name, Temperature, Humidity, Pressure, Description
        """
        if not isinstance(city, str):
            return "City Must Be A String"
        if self.unit is not None:
            if self.unit.lower() not in self._avialable_units:
                return 'Please Select Correct Temperature Unit'
        city = city
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'ab7530ca68e28e96f7cd8f21c6cc0f93'
        URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
        try:
            response = requests.get(URL)
        except Exception:
            return 'Can\'t Fetch Weather, Something Went Wrong!'
        data = response.json()
        if data['cod'] == "404":
            return 'City Not Found!'
        weather_data = data['main']
        kelvin = round(weather_data['temp'])
        celsius = round(kelvin - 273)
        fahrenheit = round((kelvin - 273) * (9 / 5) + 32)
        kelvin, celsius, fahrenheit = str(kelvin) + '°K', str(celsius) + "°C", str(fahrenheit) + "°F"
        pressure = weather_data['pressure']
        humidity = weather_data['humidity']
        weather = data['weather']
        description = weather[0]['description']
        if only_temp and self.unit == None:
            return 'Please Specify Temperature Unit'
        if self.unit != None:
            if only_temp == True:
                if self.unit == 'kelvin':
                    return kelvin
                elif self.unit == 'celsius':
                    return celsius
                elif self.unit == 'fahrenheit':
                    return fahrenheit

        if self.unit is None:
            return ({
                'City: ': city,
                'Temperature In Kelvin: ': kelvin,
                'Temperature In Celsius: ': celsius,
                'Temperature In Fahrenheit: ': fahrenheit,
                'Pressure: ': pressure,
                'Humidity: ': humidity,
                'Description: ': description
            })
        if self.unit.lower() == 'kelvin':
            return ({
                'City: ': city,
                'Temperature : ': kelvin,
                'Pressure: ': pressure,
                'Humidity: ': humidity,
                'Description: ': description
            })
        elif self.unit.lower() == 'celsius':
            return ({
                'City: ': city,
                'Temperature: ': celsius,
                'Pressure: ': pressure,
                'Humidity: ': humidity,
                'Description: ': description
            })
        elif self.unit.lower() == 'fahrenheit':
            return ({
                'City: ': city,
                'Temperature: ': fahrenheit,
                'Pressure: ': pressure,
                'Humidity: ': humidity,
                'Description: ': description
            })

    def fetch_multiple_city_weather(self, lst):
        """
        takes a list of city as parameter and returns a table containing City name, Temperature, Humidity, Pressure, Description
        :param lst: List Of City Names
        :return: Returns a table with Temperature, Humidity, Pressure, Description, City Name
        """
        print('Fetching Weather Data', end='', flush=True)
        for i in range(1, 12 + 1):
            print('.', end='', flush=True)
            time.sleep(0.3)
        if sys.platform == 'linux':
            os.system('clear')
        elif sys.platform == 'win32':
            os.system('cls')
        try:
            from prettytable import PrettyTable
        except ImportError:
            return "Prettytable Not Found Please Install Using Command [ pip install prettytable ]\n" \
                   "You Cant Use This Function Without prettytable"
        if not lst:
            return "List Is Empty"
        if self.unit is None:
            return 'Please Specify a Temperature unit For using This Function'
        table = PrettyTable(field_names=['City', 'Temperature', 'Pressure', 'Humidity', 'Description'],
                            title='Weather Data')
        for i in lst:
            rows = []
            data = self.fetch_weather(i)
            if data == 'Please Select Correct Temperature Unit':
                return "Please Select Correct Temperature Unit"
            elif data == 'Can\'t Fetch Weather, Something Went Wrong!':
                return "Can\'t Fetch Weather, Something Went Wrong!"
            elif data == 'City Not Found!':
                return f'{i} City Was Not Found!'
            if isinstance(data, dict):
                for j in data.values():
                    rows.append(j)
                table.add_row(rows)
            else:
                return 'Unknown Error'
        return table


__version__ = '1.6'
__author__ = "Patan Musthakheem Khan"
__licence__ = 'Apache 2.0'
