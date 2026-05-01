// Define the API root for weather information
const apiRoot = 'http://api.openweathermap.org/data/2.5/';

// Get the API keys from local storage
const apiKey = localStorage.getItem('openweathermap_api_key');

// Define the API endpoint for geolocation
const geoApiEndpoint = `https://ipapi.co/json/?access_key=YOUR_ACCESS_KEY`;

// Function to get the location's geolocation data
async function getGeoData() {
    try {
        const response = await fetch(geoApiEndpoint);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching geo data:', error);
        return null;
    }
}

// Function to fetch weather data for a given city
async function getWeatherData(cityName) {
    try {
        const response = await fetch(`${apiRoot}weather?q=${cityName}&appid=${apiKey}&units=metric`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching weather data:', error);
        return null;
    }
}

// Function to fetch forecast data for a given city
async function getForecastData(cityName) {
    try {
        const response = await fetch(`${apiRoot}forecast?q=${cityName}&appid=${apiKey}&units=metric`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching forecast data:', error);
        return null;
    }
}

// Function to update the forecast UI
function updateForecastUI(data) {
    const forecastList = document.getElementById('forecast-list');
    forecastList.innerHTML = '';
    data.list.forEach((item) => {
        const itemHTML = `
            <li>
                <p>Day: ${item.dt_txt}</p>
                <p>Temperature: ${item.main.temp}°C</p>
                <p>Conditions: ${item.weather[0].description}</p>
            </li>
        `;
        forecastList.innerHTML += itemHTML;
    });
}

// Function to update the current weather UI
function updateWeatherUI(data) {
    const weatherElement = document.getElementById('weather');
    weatherElement.innerHTML = `
        <h2>Current Weather in ${data.name}</h2>
        <p>Temperature: ${data.main.temp}°C</p>
        <p>Description: ${data.weather[0].description}</p>
        <p>Humidity: ${data.main.humidity}%</p>
    `;
}

// Get the location's geolocation data
getGeoData().then((data) => {
    if (data) {
        // Get the city name from the geolocation data
        const cityName = data.city;
        // Fetch the weather data for the city
        getWeatherData(cityName).then((weatherData) => {
            if (weatherData) {
                updateWeatherUI(weatherData);
                // Fetch the forecast data for the city
                getForecastData(cityName).then((forecastData) => {
                    if (forecastData) {
                        updateForecastUI(forecastData);
                    }
                });
            }
        });
    }
});