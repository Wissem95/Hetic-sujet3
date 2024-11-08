// Configuration de l'API
const API_URL = 'http://127.0.0.1:5000/api';

// Éléments du DOM
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const addCity = document.getElementById('addCity');
const addTemp = document.getElementById('addTemp');
const addHumidity = document.getElementById('addHumidity');
const addDescription = document.getElementById('addDescription');
const addBtn = document.getElementById('addBtn');
const weatherResult = document.getElementById('weatherResult');
const historyResult = document.getElementById('historyResult');
const statsResult = document.getElementById('statsResult');
const analyticsResult = document.getElementById('analyticsResult');
const trendsResult = document.getElementById('trendsResult');
const suggestionsList = document.getElementById('suggestionsList');

// Fonction pour obtenir l'icône météo appropriée
function getWeatherIcon(description) {
    description = description.toLowerCase();
    if (description.includes('soleil') || description.includes('ensoleillé') || description.includes('clair')) {
        return '<i class="fas fa-sun weather-icon sunny"></i>';
    } else if (description.includes('nuage') || description.includes('couvert')) {
        return '<i class="fas fa-cloud weather-icon cloudy"></i>';
    } else if (description.includes('pluie') || description.includes('pluvieux')) {
        return '<i class="fas fa-cloud-rain weather-icon rainy"></i>';
    } else if (description.includes('orage')) {
        return '<i class="fas fa-bolt weather-icon stormy"></i>';
    } else if (description.includes('neige')) {
        return '<i class="fas fa-snowflake weather-icon"></i>';
    } else if (description.includes('brouillard') || description.includes('brume')) {
        return '<i class="fas fa-smog weather-icon"></i>';
    } else if (description.includes('vent')) {
        return '<i class="fas fa-wind weather-icon"></i>';
    }
    return '<i class="fas fa-cloud weather-icon"></i>'; // Icône par défaut
}

// Fonction pour formater la date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Fonction pour obtenir les suggestions
async function getCitySuggestions(query) {
    if (query.length < 2) {
        suggestionsList.innerHTML = '';
        suggestionsList.style.display = 'none';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cities/suggest/${query}`);
        const suggestions = await response.json();
        
        if (suggestions.length > 0) {
            suggestionsList.innerHTML = suggestions
                .map(city => `
                    <div class="suggestion-item">
                        <i class="fas fa-map-marker-alt"></i> ${city}
                    </div>
                `).join('');
            suggestionsList.style.display = 'block';
        } else {
            suggestionsList.innerHTML = '';
            suggestionsList.style.display = 'none';
        }

        document.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                cityInput.value = item.textContent.trim();
                suggestionsList.innerHTML = '';
                suggestionsList.style.display = 'none';
                getCurrentWeather(cityInput.value);
            });
        });
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        suggestionsList.innerHTML = '';
        suggestionsList.style.display = 'none';
    }
}

// Fonction pour obtenir la météo actuelle
async function getCurrentWeather(city) {
    try {
        // Météo actuelle
        const weatherResponse = await fetch(`${API_URL}/weather/${city}`);
        const weatherData = await weatherResponse.json();
        
        if (weatherResponse.ok) {
            weatherResult.innerHTML = `
                <div class="weather-card">
                    <h3>${weatherData.city}</h3>
                    ${getWeatherIcon(weatherData.description)}
                    <p><i class="fas fa-temperature-high"></i> Température: ${weatherData.temperature}°C</p>
                    <p><i class="fas fa-tint"></i> Humidité: ${weatherData.humidity}%</p>
                    <p><i class="fas fa-info-circle"></i> ${weatherData.description}</p>
                    <p><i class="fas fa-clock"></i> ${formatDate(weatherData.timestamp)}</p>
                </div>
            `;
        } else {
            weatherResult.innerHTML = `
                <div class="error">
                    <i class="fas fa-exclamation-circle"></i>
                    ${weatherData.error}
                </div>
            `;
        }

        // Historique
        const historyResponse = await fetch(`${API_URL}/weather/${city}/history`);
        const historyData = await historyResponse.json();
        
        if (historyResponse.ok) {
            historyResult.innerHTML = `
                <h3><i class="fas fa-history"></i> Historique</h3>
                ${historyData.map(data => `
                    <div class="history-card">
                        ${getWeatherIcon(data.description)}
                        <p><i class="fas fa-temperature-high"></i> ${data.temperature}°C</p>
                        <p><i class="fas fa-tint"></i> ${data.humidity}%</p>
                        <p><i class="fas fa-info-circle"></i> ${data.description}</p>
                        <p><i class="fas fa-clock"></i> ${formatDate(data.timestamp)}</p>
                    </div>
                `).join('')}
            `;
        }

        // Statistiques
        const statsResponse = await fetch(`${API_URL}/weather/${city}/stats`);
        const statsData = await statsResponse.json();
        
        if (statsResponse.ok) {
            statsResult.innerHTML = `
                <div class="stats-card">
                    <h3><i class="fas fa-chart-bar"></i> Statistiques</h3>
                    <div class="stat-item">
                        <i class="fas fa-temperature-high"></i>
                        <span>Température moyenne: ${statsData.average_temperature.toFixed(1)}°C</span>
                    </div>
                    <div class="stat-item">
                        <i class="fas fa-arrow-up"></i>
                        <span>Maximum: ${statsData.max_temperature}°C</span>
                    </div>
                    <div class="stat-item">
                        <i class="fas fa-arrow-down"></i>
                        <span>Minimum: ${statsData.min_temperature}°C</span>
                    </div>
                    <div class="stat-item">
                        <i class="fas fa-database"></i>
                        <span>Nombre de relevés: ${statsData.number_of_records}</span>
                    </div>
                </div>
            `;
        }

        // Analytics et Trends
        const analyticsResponse = await fetch(`${API_URL}/weather/${city}/analytics`);
        const analyticsData = await analyticsResponse.json();
        const trendsResponse = await fetch(`${API_URL}/weather/${city}/trends`);
        const trendsData = await trendsResponse.json();

        if (analyticsResponse.ok && analyticsData.length > 0) {
            analyticsResult.innerHTML = `
                <div class="analytics-card">
                    <h3><i class="fas fa-chart-line"></i> Analyses sur 24h</h3>
                    ${analyticsData.map(hour => `
                        <div class="analytics-item">
                            <p><i class="fas fa-clock"></i> ${formatDate(hour.hour)}</p>
                            <p><i class="fas fa-temperature-high"></i> ${hour.avg_temp.toFixed(1)}°C</p>
                            <p><i class="fas fa-chart-bar"></i> ${hour.data_points} mesures</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        if (trendsResponse.ok && trendsData.length > 0) {
            trendsResult.innerHTML = `
                <div class="trends-card">
                    <h3><i class="fas fa-chart-trend-up"></i> Tendances</h3>
                    ${trendsData.map(day => `
                        <div class="trend-item">
                            <p><i class="fas fa-calendar-day"></i> ${formatDate(day.day)}</p>
                            <p><i class="fas fa-temperature-high"></i> ${day.avg_temp.toFixed(1)}°C</p>
                            <p><i class="fas fa-exchange-alt"></i> Variation: ${day.temp_change ? day.temp_change.toFixed(1) + '°C' : 'N/A'}</p>
                        </div>
                    `).join('')}
                </div>
            `;
        }

    } catch (error) {
        console.error('Error:', error);
        weatherResult.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-circle"></i>
                Erreur lors de la récupération des données
            </div>
        `;
    }
}

// Fonction pour ajouter des données météo
async function addWeatherData() {
    const data = {
        city: addCity.value,
        temperature: parseFloat(addTemp.value),
        humidity: parseInt(addHumidity.value),
        description: addDescription.value
    };

    try {
        const response = await fetch(`${API_URL}/weather`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (response.ok) {
            addCity.value = '';
            addTemp.value = '';
            addHumidity.value = '';
            addDescription.value = '';
            getCurrentWeather(data.city);
        } else {
            alert(`Erreur: ${result.error}`);
        }
    } catch (error) {
        alert('Erreur lors de l\'ajout des données');
    }
}

// Événements
let debounceTimer;
cityInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        getCitySuggestions(e.target.value.trim());
    }, 300);
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) {
        suggestionsList.innerHTML = '';
        suggestionsList.style.display = 'none';
    }
});

searchBtn.addEventListener('click', () => {
    const city = cityInput.value.trim();
    if (city) {
        getCurrentWeather(city);
    }
});

addBtn.addEventListener('click', addWeatherData);

cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = cityInput.value.trim();
        if (city) {
            getCurrentWeather(city);
        }
    }
});