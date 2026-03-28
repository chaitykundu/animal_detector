from pydantic import BaseModel
from typing import List

class Animal(BaseModel):
    Unique_ID: str
    Animal_Species: str
    Gender: str
    Age: str
    Health_Status: str
    Observations: str