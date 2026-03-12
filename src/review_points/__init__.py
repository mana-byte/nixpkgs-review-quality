import os
from enum import Enum

DB_URL = os.getenv('DB_URL', 'sqlite:///src/review_points/review_points.db')

class REVIEW_POINTS_TOPIC(str, Enum):
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    RUST = "Rust"
    GO = "Go"

    @classmethod
    def builder_to_topic(cls, builder_pattern: str) -> 'REVIEW_POINTS_TOPIC | None':
        builder_to_topic_mapping = {
            "buildPythonPackage": cls.PYTHON,
            "buildPythonApplication": cls.PYTHON,
            "buildNpmPackage": cls.JAVASCRIPT,
            "buildRustPackage": cls.RUST,
            "buildGoModule": cls.GO,
        }
        return builder_to_topic_mapping.get(builder_pattern, None)

