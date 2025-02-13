import streamlit as st
import requests

# Function to get weather data from OpenWeatherMap API
def get_weather(city, api_key):
    # URL to fetch the weather data from OpenWeatherMap
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"  # `units=metric` to get temperature in Celsius
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
            # If 'main' or 'weather' is not in the response, print the response for debugging
            print(data)  # Print the response to the console (can help with debugging)
            return None
    else:
        # Handle the error if the API response is not successful
        print(f"Error fetching data: {response.status_code}")  # Log the status code
        return None

# Streamlit app UI
def main():
    st.title("Weather Forecasting App")
    st.markdown("Enter the city name below to get real-time weather information.")

    # Input box for the city name
    city = st.text_input("City Name", "London")  # Default to London

    # OpenWeatherMap API key (your provided key)
    api_key = "88cc679aa867f28dfc12e493b3f4fec1"

    # When the user presses the 'Get Weather' button
    if st.button("Get Weather"):
        if city:
            # Fetch weather data
            weather_data = get_weather(city, api_key)
            
            if weather_data:
                # Display weather details
                st.subheader(f"Weather in {weather_data['city']}")
                st.image(f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png", width=100)
                st.write(f"**Temperature**: {weather_data['temperature']} °C")
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
