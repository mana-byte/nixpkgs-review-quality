import os
from enum import Enum

DB_URL = os.getenv('DB_URL', 'sqlite:///src/review_points/review_points.db')

class REVIEW_POINTS_TOPIC(str, Enum):
    PYTHON = "Python"
