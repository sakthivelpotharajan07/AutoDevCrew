import requests
import json

def get_weather_api_data(api_key, city_name):
    """
    Function to fetch weather data from API.
    
    Parameters:
    api_key (str): API key for weather data
    city_name (str): Name of the city
    
    Returns:
    dict: Dictionary containing weather data
    """
    
    # API endpoint URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    
    try:
        # Send GET request
        response = requests.get(url)
        
        # Check if response is valid
        if response.status_code == 200:
            # Parse JSON data
            weather_data = response.json()
            
            return weather_data
        else:
            raise Exception('Failed to fetch weather data')
    except requests.exceptions.RequestException as e:
        # Handle exceptions
        print(f'Error occurred: {str(e)}')