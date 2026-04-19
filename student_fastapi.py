#import libraries
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import sqlite3

#load model
model=joblib.load("student_model.pkl")
scaler=joblib.load("student_scaler.pkl")

class Student(BaseModel):
    hours_studied:float
    sleep_hours:float
    previous_score:float
    
app=FastAPI()
@app.get("/")
def home():
    return {"Message":"Running ML API"}
@app.post("/prediction")
def predict(data:Student):
    features=[[data.hours_studied,data.sleep_hours,data.previous_score]]
    features=scaler.transform(features)
    prediction=model.predict(features)[0]

    #store prediction in sqlite
    conn=sqlite3.connect("predictions.db")
    cursor=conn.cursor()
    #create table to store input and result
    cursor.execute("""CREATE TABLE IF NOT EXISTS Predictions (
                  study_hours REAL,
                  sleep REAL,
                  prev_score REAL,
                  result REAL)"""
              )
    cursor.execute("INSERT INTO Predictions VALUES(?,?,?,?)",(data.hours_studied,data.sleep_hours,data.previous_score,float(prediction)))
    conn.commit()
    conn.close()
    return {"prediction":prediction}

   #file logging
    import logging
    logging.basicConfig(filename="logs.log",level=logging.INFO)
    logging.info(f"input:{features},prediction:{prediction}")