import os
from dotenv import load_dotenv
import streamlit as st
import requests

# Load environment variables (for API key)
load_dotenv()

# Function to get weather data from OpenWeatherMap API
def get_weather(city, api_key, units="metric"):
    # URL to fetch the weather data from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units={units}"  # Unit can be metric, imperial, or standard
    response = requests.get(complete_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if the response contains 'main' and 'weather' keys
        if 'main' in data and 'weather' in data:
            main = data['main']
            wind = data['wind']
            weather = data['weather'][0]
            
            # Extracting necessary information
            city_name = data['name']
            temperature = main['temp']
            pressure = main['pressure']
            humidity = main['humidity']
            wind_speed = wind['speed']
            description = weather['description']
            icon = weather['icon']

            # Return all the details we want to show
            return {
                "city": city_name,
                "temperature": temperature,
                "pressure": pressure,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "description": description,
                "icon": icon
            }
        else:
            return None
    else:
        return None

# Streamlit app UI
def main():
    st.title("Weather Forecasting App")
    st.markdown("Enter the city name below to get real-time weather information.")

    # Input box for the city name
    city = st.text_input("Enter City Name", "")  # Empty input by default

    # Dropdown to select units
    units = st.selectbox("Select Temperature Units", ["metric (Celsius)", "imperial (Fahrenheit)", "standard (Kelvin)"])

    # OpenWeatherMap API key (loaded from .env)
    api_key = os.getenv("API_KEY")

    # When the user presses the 'Get Weather' button
    if st.button("Get Weather"):
        if city:
            # Fetch weather data
            weather_data = get_weather(city, api_key, units=units.split()[0].lower())
            
            if weather_data:
                # Display weather details
                st.subheader(f"Weather in {weather_data['city']}")
                st.image(f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png", width=100)
                st.write(f"**Temperature**: {weather_data['temperature']}°")
                st.write(f"**Description**: {weather_data['description']}")
                st.write(f"**Pressure**: {weather_data['pressure']} hPa")
                st.write(f"**Humidity**: {weather_data['humidity']} %")
                st.write(f"**Wind Speed**: {weather_data['wind_speed']} m/s")
            else:
                st.error("Could not retrieve weather data. Please check the city name or try again later.")
        else:
            st.warning("Please enter a city name.")

if __name__ == "__main__":
    main()

