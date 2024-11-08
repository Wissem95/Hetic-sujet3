from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
import os
from config import Config
from models.weather import db, WeatherData
from api.weather_service import WeatherService

app = Flask(__name__, static_folder='../frontend')
app.config.from_object(Config)
CORS(app)

# Initialisation de la base de données et du service météo
db.init_app(app)
migrate = Migrate(app, db)
weather_service = WeatherService()

# Route racine qui sert index.html
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Route pour servir les fichiers CSS et JS
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Nouvelle route pour l'autocomplétion des villes
@app.route('/api/cities/suggest/<query>')
def suggest_cities(query):
    try:
        suggestions = weather_service.get_city_suggestions(query)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return {'status': 'ok'}

@app.route('/api/weather', methods=['POST'])
def add_weather():
    data = request.get_json()
    
    if not all(key in data for key in ['city', 'temperature']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = weather_service.add_weather_data(
            city=data['city'],
            temperature=data['temperature'],
            humidity=data.get('humidity'),
            description=data.get('description')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    weather = weather_service.get_current_weather(city)
    if weather:
        return jsonify(weather.to_dict())
    return jsonify({'error': 'City not found'}), 404

@app.route('/api/weather/<city>/history', methods=['GET'])
def get_weather_history(city):
    weathers = weather_service.get_weather_history(city)
    return jsonify([w.to_dict() for w in weathers])

@app.route('/api/weather/<city>/stats', methods=['GET'])
def get_city_stats(city):
    stats = weather_service.get_city_statistics(city)
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'No data found for this city'}), 404

@app.route('/api/weather/<city>/analytics')
def get_weather_analytics(city):
    try:
        analytics = weather_service.get_weather_analytics(city)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/<city>/trends')
def get_city_trends(city):
    days = request.args.get('days', default=7, type=int)
    try:
        trends = weather_service.get_city_trends(city, days)
        return jsonify([dict(row) for row in trends])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/<int:weather_id>', methods=['PUT'])
def update_weather(weather_id):
    data = request.get_json()
    try:
        result = weather_service.update_weather_data(
            weather_id,
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            description=data.get('description')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/weather/<int:weather_id>', methods=['DELETE'])
def delete_weather(weather_id):
    try:
        weather_service.delete_weather_data(weather_id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)