# Python Terminal Weather App ⛅

A robust command-line application that fetches real-time weather data and a 5-day extended forecast for any city in the world using the OpenWeather API. 

This project goes beyond basic API fetching by implementing mathematical logic to calculate true daily highs and lows, converting wind degrees to cardinal directions, and securely managing API credentials.

## 🚀 Features

* **Current Weather Data:** Displays temperature, "feels like" temperature, humidity, and atmospheric conditions.
* **True 5-Day Forecast:** Groups 3-hour interval API data into calendar days to calculate true daily maximum and minimum temperatures.
* **Wind Direction Mapping:** Uses modular arithmetic to convert raw wind degrees (0-360°) into 16 cardinal compass directions (N, NE, SW, etc.).
* **Smart Suggestions:** Provides dynamic clothing and activity recommendations based on the current temperature and weather conditions (e.g., bringing an umbrella, dressing warmly).
* **Unit Conversions:** Seamlessly calculates and displays temperatures in both Celsius and Fahrenheit.
* **Visual Icons:** Automatically opens the official OpenWeather condition icon in your default web browser.
* **Secure Key Management:** Uses `python-dotenv` to keep API keys hidden and secure.

## 📋 Prerequisites

* **Python 3.7 or higher** installed on your machine.
* A free API key from [OpenWeatherMap](https://openweathermap.org/api).
* Git (optional, for cloning the repository).