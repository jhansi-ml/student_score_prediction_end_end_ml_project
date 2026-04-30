#import libraries
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import sqlite3
from datetime import datetime
    
#load model
model=joblib.load("student_model.pkl")
scaler=joblib.load("student_scaler.pkl")

#store prediction in sqlite
conn=sqlite3.connect("predictions.db",check_same_thread=False)
cursor=conn.cursor()
#create table to store input and result
cursor.execute("""CREATE TABLE IF NOT EXISTS Prediction (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  study_hours REAL,
                  sleep REAL,
                  prev_score REAL,
                  result REAL,
                  created_at TEXT)"""
              )
conn.commit()

class Student(BaseModel):
    hours_studied:float
    sleep_hours:float
    previous_score:float
    
app=FastAPI()
@app.get("/")
def home():
    return {"Message":"Running ML API"}

@app.get("/sample")
def sample_input():
    return {
        "sample input":{
             "hours_studied":5,
             "sleep_hours":6,
             "previous_score":60
        }}
    
@app.post("/prediction")
def predict(data:Student):
    features=[[data.hours_studied,data.sleep_hours,data.previous_score]]
    features=scaler.transform(features)
    prediction=model.predict(features)[0]

    #inser into database
    cursor.execute("""INSERT INTO Prediction 
    (study_hours, 
    sleep, 
    prev_score, 
    result, 
    created_at)
    VALUES (?, ?, ?, ?, ?)""",(
    data.hours_studied,
    data.sleep_hours,
    data.previous_score,
    float(prediction),
    datetime.now().isoformat()
    ))
    conn.commit()
    
    return {"prediction":prediction}
     
#view logs
@app.get("/logs")
def get_logs():
    cursor.execute("SELECT *FROM Prediction ORDER BY id DESC")
    rows=cursor.fetchall()
    res=[]
    for row in rows:
        res.append({
        "id":row[0],
        "input":{"study_hours": row[1],
                 "sleep": row[2],
                 "prev_score": row[3]},
        "prediction":row[4],
        "time":row[5]
        })
    return {
        "total_rows":len(res),
        "rows":res
    }
