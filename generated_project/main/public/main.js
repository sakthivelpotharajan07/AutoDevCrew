const forecastElement = document.getElementById('forecast');

function displayWeatherData(data) {
    const currentElement = document.getElementById('current-weather');
    currentElement.innerHTML = `
        <h2>Current weather in ${data.city.name}</h2>
        <p>Temperature: ${data.current.temp_c}°C</p>
        <p>Conditions: ${data.current.condition.text}</p>
    `;

    const forecastList = document.createElement('ul');
    data.forecast.forecastday.forEach((day, index) => {
        const listItem = document.createElement('li');
        const dateText = document.createTextNode(`${new Date(day.date).toLocaleString('default', {day: 'numeric', month: 'long'})}`);
        const conditionText = document.createTextNode(day.day.condition.text);
        const highText = document.createTextNode(`High: ${day.day.maxtemp_c}°C`);
        const lowText = document.createTextNode(`Low: ${day.day.mintemp_c}°C`);

        listItem.appendChild(dateText);
        listItem.appendChild(document.createTextNode(' '));
        listItem.appendChild(conditionText);
        listItem.appendChild(document.createTextNode(' '));
        listItem.appendChild(highText);
        listItem.appendChild(document.createTextNode(' - '));
        listItem.appendChild(lowText);

        forecastList.appendChild(listItem);
    });

    forecastElement.appendChild(forecastList);
}

fetch('https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=Halifax')
    .then(response => response.json())
    .then(data => displayWeatherData(data));

fetch('https://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q=Halifax')
    .then(response => response.json())
    .then(data => displayWeatherData(data));