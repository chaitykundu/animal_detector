from pydantic import BaseModel
from typing import Optional, List

class AntlersHorns(BaseModel):
    Type: Optional[str] = None           # e.g., Spiker, Palmate, 6-pointer
    Condition: Optional[str] = None      # e.g., Broken tine, uneven beams
    Notes: Optional[str] = None           # Any additional observations

class HealthDetails(BaseModel):
    Condition: str                        # Healthy, Sick, Weak, Strong
    Likely_Disease: Optional[str] = None  # Only if sick
    Management_Tips: Optional[str] = None # Only if sick

class Animal(BaseModel):
    Unique_ID: str
    Animal_Species: str
    Gender: str
    Age: str
    Health_Status: HealthDetails           # Nested model for detailed health
    Pregnancy_Status: Optional[str] = None  # Pregnant, Non-Pregnant, N/A
    Antlers_Horns: Optional[AntlersHorns] = None
    Observations: Optional[str] = None