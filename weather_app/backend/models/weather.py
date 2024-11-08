from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, text

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Optimisations Big Data avec uniquement les index
    __table_args__ = (
        Index('idx_timestamp_city', 'timestamp', 'city'),
        Index('idx_temperature_humidity', 'temperature', 'humidity'),
        Index('idx_city_temp_time', 'city', 'temperature', 'timestamp')
    )

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }