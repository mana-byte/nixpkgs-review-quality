import os

DB_URL = os.getenv('DB_URL', 'sqlite:///src/review_points/review_points.db')
