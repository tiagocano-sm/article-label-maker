from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import List

class Labels(str, Enum):
    """Schema for classification labels"""
    CARDIOVASCULAR = "Cardiovascular"
    NEUROLOGICAL = "Neurological"
    HEPATORENAL = "Hepatorenal"
    ONCOLOGICAL = "Oncological"

    @classmethod
    def get_labels(cls) -> List[str]:
        """Get all label string values"""
        return [label.value for label in cls]


class Settings(BaseSettings):
    """Settings for the application"""

    labels: List[str] = Field(description="Classification labels", default=Labels.get_labels())
    classifier_type: str = Field(description="Classifier type", default="zero_shot")
    device: str = Field(description="Device to run inference on", default="mps")
    threshold: float = Field(description="Threshold for classification", default=0.95)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

 


@lru_cache
def get_settings():
    """Get settings for the application"""
    return Settings()

settings = get_settings()