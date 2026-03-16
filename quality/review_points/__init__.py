"""
Regroups DB_URL and REVIEW_POINTS_TOPIC enum for review points module.
"""

import os
from enum import Enum

DB_URL = os.getenv("DB_URL", "sqlite:///src/review_points/review_points.db")


class REVIEW_POINTS_TOPIC(str, Enum):
    """
    Enum representing the topic of a review point. This is used to categorize review points based on the builder pattern they are associated with.
    """

    GLOBAL = "Global"
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    RUST = "Rust"
    GO = "Go"

    @classmethod
    def builder_to_topic(cls, builder_pattern: str) -> "REVIEW_POINTS_TOPIC | None":
        """Maps a builder pattern to a review points topic. If the builder pattern is not recognized, returns None."""
        builder_to_topic_mapping = {
            "buildPythonPackage": cls.PYTHON,
            "buildPythonApplication": cls.PYTHON,
            "buildNpmPackage": cls.JAVASCRIPT,
            "buildRustPackage": cls.RUST,
            "buildGoModule": cls.GO,
        }
        return builder_to_topic_mapping.get(builder_pattern, None)
