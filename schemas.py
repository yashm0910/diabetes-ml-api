from pydantic import BaseModel,Field
from typing import Optional

class DiabetesSchema(BaseModel):
    Pregnancies: int=Field(ge=0,lt=20)
    Glucose: int=Field(ge=0,lt=300)
    BMI: float=Field(ge=10,lt=70)
    BloodPressure : int=Field(ge=0,le=200)
    SkinThickness : int=Field(ge=0,le=100)
    Insulin : int=Field(ge=0,lt=900)
    DiabetesPedigree : float=Field(ge=0,le=5)
    Age : int=Field(ge=1,le=120)
    
    # ... add others here
    class Config:
        from_attributes = True
        
class DiabetesUpdate(BaseModel):
    Pregnancies: Optional[int] = Field(default=None, ge=0, le=20)
    Glucose: Optional[int] = Field(default=None, ge=0, le=300)
    BMI: Optional[float] = Field(default=None, ge=10, le=70)
    BloodPressure: Optional[int] = Field(default=None, ge=0, le=200)
    SkinThickness: Optional[int] = Field(default=None, ge=0, le=100)
    Insulin: Optional[int] = Field(default=None, ge=0, le=900)
    DiabetesPedigree: Optional[float] = Field(default=None, ge=0, le=5)
    Age: Optional[int] = Field(default=None, ge=1, le=120)
    
class Showbp(BaseModel):
    BloodPressure:int
    BMI:float
    
    class Config:
        orm_mode=True
        
class PredictionResponse(BaseModel):
    patient_id: int
    prediction: int

    class Config:
        orm_mode = True