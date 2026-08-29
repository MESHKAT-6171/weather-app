import requests
import json
import webbrowser
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the key securely
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
# https://api.openweathermap.org/data/2.5/forecast?q=Dhaka,bd&appid=8f8f61bd037f7d4d4b60901ca3b64dfa
class Location:
    

    def __init__(self, city, country=None):
        self.city = city
        self.country = country
        self.api_key = API_KEY

    def get_weather_data(self):
       
        query = f"{self.city},{self.country}" if self.country else self.city
        url = f"{BASE_URL}?q={query}&appid={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving weather data: {response.status_code}")
            return None

    def get_current_weather(self):
      
        query = f"{self.city},{self.country}" if self.country else self.city
        url = f"{CURRENT_WEATHER_URL}?q={query}&appid={self.api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving current weather data: {response.status_code}")
            return None


class ExtendedForecast:
    
    def __init__(self, weather_data):
        self.data = weather_data

    def format_extended_forecast(self, num_days=5, unit='C'):
        if self.data is None or "list" not in self.data:
            return "Error: Could not retrieve weather data."

        forecast_text = "\n**Extended 5-Day Forecast (True Highs & Lows):**\n"
        
        # Dictionary to group temperatures and conditions by date
        daily_data = {}
        
        for item in self.data["list"]:
            date = item["dt_txt"].split(" ")[0] # Extract just the YYYY-MM-DD
            temp_k = item["main"]["temp"]
            condition = item["weather"][0]["description"]
            
            if date not in daily_data:
                daily_data[date] = {"temps": [], "conditions": []}
                
            daily_data[date]["temps"].append(temp_k)
            daily_data[date]["conditions"].append(condition)

        # Calculate high and low for each day
        day_count = 1
        for date, info in daily_data.items():
            if day_count > num_days:
                break
                
            min_k = min(info["temps"])
            max_k = max(info["temps"])
            
            # Find the most frequent weather condition for that day
            main_condition = max(set(info["conditions"]), key=info["conditions"].count)
            
            if unit == 'F':
                low = TemperatureConverter(min_k - 273.15).convert_to_fahrenheit()
                high = TemperatureConverter(max_k - 273.15).convert_to_fahrenheit()
                sym = "°F"
            else:
                low = round(min_k - 273.15, 2)
                high = round(max_k - 273.15, 2)
                sym = "°C"
                
            forecast_text += f"  - {date}: Low {low}{sym} / High {high}{sym} | {main_condition}\n"
            day_count += 1

        location_info = self.get_location_info()
        forecast_text += f"\n**Location Information:**\n"
        forecast_text += f"  - Latitude: {location_info['lat']}\n"
        forecast_text += f"  - Longitude: {location_info['lon']}\n"
        forecast_text += f"  - Timezone: {location_info['timezone']}\n"

        return forecast_text

    def get_location_info(self):
        if "city" in self.data and "coord" in self.data["city"]:
            return {
                "lat": self.data["city"]["coord"]["lat"],
                "lon": self.data["city"]["coord"]["lon"],
                "timezone": self.data["city"]["timezone"]
            }
        else:
            return {"lat": None, "lon": None, "timezone": None}


class TemperatureConverter:
   

    def __init__(self, temperature):
        self.temperature = temperature

    def convert_to_fahrenheit(self):
       
        return round((self.temperature * 9/5) + 32, 2)

    def convert_to_celsius(self):
       
        return round((self.temperature - 32) * 5/9, 2)


def get_cardinal_direction(degrees):
    # A compass has 16 primary directions, each taking up 22.5 degrees (360 / 16).
    # We shift by 11.25 (which is 22.5 / 2) to perfectly center the directions, 
    # then use modulo 16 to wrap around from North to North.
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    index = round(degrees / 22.5) % 16
    return dirs[index]

def get_weather_suggestions(weather_data):
   
    if weather_data is None:
        return "Error: No weather data available."

    current_temp_kelvin = weather_data["main"]["temp"]
    current_temp_celsius = round(current_temp_kelvin - 273.15, 2)
    weather_description = weather_data["weather"][0]["description"]

    suggestions = f"Current temperature is {current_temp_celsius:.2f}°C with {weather_description}.\n"

    if "rain" in weather_description:
        suggestions += "It's raining, don't forget to carry an umbrella!\n"
    elif "clear" in weather_description:
        suggestions += "It's clear outside, a great day for outdoor activities!\n"
    elif "snow" in weather_description:
        suggestions += "It's snowing, dress warmly and be careful on the roads!\n"
    elif "clouds" in weather_description:
        suggestions += "It's cloudy, might be a bit gloomy outside.\n"
    elif "thunderstorm" in weather_description:
        suggestions += "There's a thunderstorm, stay indoors and be safe!\n"
    elif current_temp_celsius < 0:
        suggestions += "It's freezing, dress warmly!\n"
    elif current_temp_celsius > 30:
        suggestions += "It's quite hot, stay hydrated!\n"
    else:
        suggestions += "The weather is moderate, have a great day!\n"

    return suggestions


def display_weather_icon(weather_data):
   
    if weather_data is None:
        return

    icon_code = weather_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    webbrowser.open(icon_url)


# Example usage

city = input("Enter city name: ")
country = input("Enter country code (optional, press Enter to skip): ").strip() or None

location = Location(city, country)
weather_data = location.get_weather_data()
current_weather_data = location.get_current_weather()


if current_weather_data:
    print("Current Weather:")
    current_temp_kelvin = current_weather_data["main"]["temp"]
    current_temp_celsius = round(current_temp_kelvin - 273.15, 2)
    current_temp_fahrenheit = TemperatureConverter(current_temp_celsius).convert_to_fahrenheit()
    
    min_temp_kelvin = current_weather_data["main"]["temp_min"]
    min_temp_celsius = round(min_temp_kelvin - 273.15, 2)
    min_temp_fahrenheit = TemperatureConverter(min_temp_celsius).convert_to_fahrenheit()
    
    max_temp_kelvin = current_weather_data["main"]["temp_max"]
    max_temp_celsius = round(max_temp_kelvin - 273.15, 2)
    max_temp_fahrenheit = TemperatureConverter(max_temp_celsius).convert_to_fahrenheit()
    
    feels_like_kelvin = current_weather_data["main"]["feels_like"]
    feels_like_celsius = round(feels_like_kelvin - 273.15, 2)
    feels_like_fahrenheit = TemperatureConverter(feels_like_celsius).convert_to_fahrenheit()
    
    humidity = current_weather_data["main"]["humidity"]
    wind_speed = current_weather_data["wind"]["speed"]
    wind_deg = current_weather_data["wind"]["deg"]
    
    
    weather_description = current_weather_data["weather"][0]["description"]
    print(f"  - Temperature: {current_temp_celsius}°C / {current_temp_fahrenheit}°F")
    print(f"  - Min Temperature: {min_temp_celsius}°C / {min_temp_fahrenheit}°F")
    print(f"  - Max Temperature: {max_temp_celsius}°C / {max_temp_fahrenheit}°F")
    

    print(f"  - Feels Like: {feels_like_celsius}°C / {feels_like_fahrenheit}°F")
    print(f"  - Humidity: {humidity}%")
    wind_deg = current_weather_data["wind"]["deg"]
    wind_direction = get_cardinal_direction(wind_deg)
    
    print(f"  - Wind Speed: {wind_speed} m/s")
    print(f"  - Wind Direction: {wind_deg}° ({wind_direction})")
    
    #print(f"  - Wind Speed: {wind_speed} m/s")
    #print(f"  - Wind Direction: {wind_deg}°")
    print(f"  - Condition: {weather_description}")

    display_weather_icon(current_weather_data)

    suggestions = get_weather_suggestions(current_weather_data)
    print(suggestions)

unit = input("Enter temperature unit (C for Celsius, F for Fahrenheit): ").strip().upper()
see_all_forecast = input("Do you want to see all outputs of the extended forecast? (yes/no): ").strip().lower()
if see_all_forecast == 'yes' and weather_data:
    forecast = ExtendedForecast(weather_data)
    print(forecast.format_extended_forecast(unit=unit, num_days=15))
else:
    print("Failed to retrieve weather data.")
