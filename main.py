from fastapi import FastAPI,Depends,HTTPException,status
from database import engine,Base
import models
from models import *
from database import engine,SessionLocal
from sqlalchemy.orm import session
import schemas
from sqlalchemy.orm import Session,Query
import joblib

model=joblib.load("diabetes_model.pkl")
scaler = joblib.load("diabetes_scaler.pkl")

app=FastAPI()


# Create the tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Database and Tables Created!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_patient")
def create(request:schemas.DiabetesSchema ,db:session=Depends(get_db)):
    new_patient=models.DiabetesModel(
        BMI=request.BMI,
        BloodPressure=request.BloodPressure,
        Pregnancies=request.Pregnancies,
        Glucose=request.Glucose,
        SkinThickness=request.SkinThickness,
        Insulin=request.Insulin,
        DiabetesPedigree=request.DiabetesPedigree,
        Age=request.Age
        )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return new_patient

@app.get("/patient")
def get(db:session=Depends(get_db)):
    patients=db.query(models.DiabetesModel).order_by(models.DiabetesModel).all()
    return patients

@app.patch("/patients/{id}")
def update_patient(id:int,request:schemas.DiabetesUpdate,db:session=Depends(get_db)):
    patient=db.query(models.DiabetesModel).filter(models.DiabetesModel.id==id).first()
    
    if not patient:
        raise HTTPException(status_code=404,detail="patient not found")
    
    update_data=request.dict(exclude_unset=True)
    
    for k,v in update_data.items():
        setattr(patient,k,v)
        
    db.commit()
    db.refresh(patient)
    
    return patient

@app.delete("/patients/{id}",status_code=status.HTTP_200_OK)
def delete_patient(id:int,db:session=Depends(get_db)):
    patient=db.query(models.DiabetesModel).filter(
        models.DiabetesModel.id==id).delete(
            synchronize_session=False)
        
    db.commit()
    return "deleted"

@app.get("/patient/getbp/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Showbp)
def get_patient_bp(id:int,db:session=Depends(get_db)):
    patients=(db.query(models.DiabetesModel)
              .order_by(models.DiabetesModel.id==id)
              .first()
    )
    return patients

@app.post("/predict/{patient_id}",response_model=schemas.PredictionResponse)
def predict(patient_id:int,db: session = Depends(get_db)):
    patient = db.query(models.DiabetesModel).filter(
        models.DiabetesModel.id == patient_id
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    features = [[
        patient.Pregnancies,
        patient.Glucose,
        patient.BloodPressure,
        patient.SkinThickness,
        patient.Insulin,
        patient.BMI,
        patient.DiabetesPedigree,
        patient.Age
    ]]
    
    scaled_features = scaler.transform(features)
    prediction_value = int(model.predict(scaled_features)[0])
    
    existing = db.query(models.DiabetesPrediction).filter(
        models.DiabetesPrediction.patient_id == patient_id
    ).first()
    
    if existing:
        existing.prediction = prediction_value
    else:
        new_prediction = models.DiabetesPrediction(
            patient_id=patient_id,
            prediction=prediction_value
        )
        db.add(new_prediction)

    db.commit()

    
    return {
        "patient_id": patient_id,
        "prediction": prediction_value
    }
