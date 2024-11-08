from datetime import datetime, timedelta
from sqlalchemy import func, text
from models.weather import db, WeatherData

class WeatherService:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes

    def get_cached_data(self, key):
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_timeout):
                return data
        return None

    def set_cached_data(self, key, data):
        self.cache[key] = (data, datetime.now())

    def get_city_suggestions(self, query):
        """
        Retourne une liste de suggestions de villes basée sur la requête
        """
        try:
            # Recherche les villes qui commencent par la requête
            cities = db.session.query(WeatherData.city)\
                .filter(WeatherData.city.ilike(f'{query}%'))\
                .distinct()\
                .order_by(WeatherData.city)\
                .limit(5)\
                .all()
            
            # Convertit les résultats en liste
            return [city[0] for city in cities]
        except Exception as e:
            print(f"Error in city suggestions: {str(e)}")
            return []

    def add_weather_data(self, city, temperature, humidity=None, description=None):
        """
        Ajoute de nouvelles données météo dans la base de données
        """
        try:
            weather_data = WeatherData(
                city=city,
                temperature=float(temperature),
                humidity=humidity,
                description=description
            )
            
            db.session.add(weather_data)
            db.session.commit()
            return weather_data.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de l'ajout des données météo: {str(e)}")

    def get_current_weather(self, city):
        """
        Récupère les dernières données météo pour une ville
        """
        cache_key = f"current_{city}"
        cached_data = self.get_cached_data(cache_key)
        if cached_data:
            return cached_data

        result = WeatherData.query.filter_by(city=city)\
            .order_by(WeatherData.timestamp.desc())\
            .first()
        
        if result:
            self.set_cached_data(cache_key, result)
        return result

    def get_weather_history(self, city, limit=10):
        """
        Récupère l'historique météo d'une ville
        """
        cache_key = f"history_{city}_{limit}"
        cached_data = self.get_cached_data(cache_key)
        if cached_data:
            return cached_data

        result = WeatherData.query.filter_by(city=city)\
            .order_by(WeatherData.timestamp.desc())\
            .limit(limit)\
            .all()
        
        self.set_cached_data(cache_key, result)
        return result

    def get_weather_analytics(self, city):
        """Analyse avancée des données météo"""
        try:
            query = text("""
                WITH hourly_stats AS (
                    SELECT 
                        date_trunc('hour', timestamp) as hour,
                        AVG(temperature) as avg_temp,
                        MIN(temperature) as min_temp,
                        MAX(temperature) as max_temp,
                        COUNT(*) as data_points,
                        AVG(humidity) as avg_humidity
                    FROM weather_data
                    WHERE city = :city
                    AND timestamp >= NOW() - INTERVAL '24 hours'
                    GROUP BY hour
                    ORDER BY hour DESC
                )
                SELECT 
                    hour,
                    avg_temp,
                    min_temp,
                    max_temp,
                    data_points,
                    avg_humidity
                FROM hourly_stats
            """)

            result = db.session.execute(query, {'city': city})
            
            # Conversion correcte en dictionnaire
            analytics = [{
                'hour': row[0].isoformat() if row[0] else None,
                'avg_temp': float(row[1]) if row[1] else None,
                'min_temp': float(row[2]) if row[2] else None,
                'max_temp': float(row[3]) if row[3] else None,
                'data_points': int(row[4]) if row[4] else 0,
                'avg_humidity': float(row[5]) if row[5] else None
            } for row in result]
            
            return analytics
        except Exception as e:
            print(f"Error in analytics: {str(e)}")
            return []

    def get_city_trends(self, city, days=7):
        """Analyse des tendances"""
        try:
            query = text("""
                WITH daily_stats AS (
                    SELECT 
                        date_trunc('day', timestamp) as day,
                        AVG(temperature) as avg_temp,
                        MIN(temperature) as min_temp,
                        MAX(temperature) as max_temp,
                        AVG(humidity) as avg_humidity,
                        COUNT(*) as measurements
                    FROM weather_data
                    WHERE city = :city
                    AND timestamp >= NOW() - INTERVAL ':days days'
                    GROUP BY day
                    ORDER BY day
                )
                SELECT 
                    day,
                    avg_temp,
                    min_temp,
                    max_temp,
                    avg_humidity,
                    measurements
                FROM daily_stats
            """)
            
            result = db.session.execute(query, {'city': city, 'days': days})
            
            # Conversion correcte en dictionnaire
            trends = [{
                'day': row[0].isoformat() if row[0] else None,
                'avg_temp': float(row[1]) if row[1] else None,
                'min_temp': float(row[2]) if row[2] else None,
                'max_temp': float(row[3]) if row[3] else None,
                'avg_humidity': float(row[4]) if row[4] else None,
                'measurements': int(row[5]) if row[5] else 0
            } for row in result]
            
            return trends
        except Exception as e:
            print(f"Error in trends: {str(e)}")
            return []

    def get_city_statistics(self, city):
        """
        Calcule des statistiques pour une ville
        """
        cache_key = f"stats_{city}"
        cached_data = self.get_cached_data(cache_key)
        if cached_data:
            return cached_data

        weathers = WeatherData.query.filter_by(city=city).all()
        if not weathers:
            return None

        temperatures = [w.temperature for w in weathers]
        stats = {
            'average_temperature': sum(temperatures) / len(temperatures),
            'max_temperature': max(temperatures),
            'min_temperature': min(temperatures),
            'number_of_records': len(temperatures)
        }
        
        self.set_cached_data(cache_key, stats)
        return stats

    def update_weather_data(self, weather_id, temperature=None, humidity=None, description=None):
        """
        Met à jour les données météo existantes
        """
        try:
            weather = WeatherData.query.get(weather_id)
            if not weather:
                raise Exception("Données météo non trouvées")

            if temperature is not None:
                weather.temperature = float(temperature)
            if humidity is not None:
                weather.humidity = humidity
            if description is not None:
                weather.description = description

            db.session.commit()
            return weather.to_dict()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la mise à jour des données météo: {str(e)}")

    def delete_weather_data(self, weather_id):
        """
        Supprime des données météo
        """
        try:
            weather = WeatherData.query.get(weather_id)
            if not weather:
                raise Exception("Données météo non trouvées")

            db.session.delete(weather)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la suppression des données météo: {str(e)}")