"""
Regroups DB_URL and REVIEW_POINTS_TOPIC enum for review points module.
"""

import os
from quality.data.enum.review_points_topic import REVIEW_POINTS_TOPIC

DB_URL = os.getenv("DB_URL", "sqlite:///quality/data/review_points.db")

__all__ = ["DB_URL", "REVIEW_POINTS_TOPIC"]
