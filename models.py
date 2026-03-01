from sqlalchemy import Column, Integer, Float,ForeignKey
from database import Base

class DiabetesModel(Base):
    __tablename__ = "diabetes_patients_data"
    
    id = Column(Integer, primary_key=True, index=True)
    Pregnancies = Column(Integer)
    Glucose = Column(Integer)
    BloodPressure = Column(Integer)
    SkinThickness = Column(Integer)
    Insulin = Column(Integer)
    BMI = Column(Float)
    DiabetesPedigree = Column(Float)
    Age = Column(Integer)
    
class DiabetesPrediction(Base):
    __tablename__="predictions"
    
    patient_id = Column(
        Integer,
        ForeignKey("diabetes_patients_data.id"),
        primary_key=True
    )

    prediction = Column(Integer)