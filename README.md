# student_score_prediction_end_end_ml_project
**🛩️Overview**  
This project is an end-to-end Machine Learning application that predicts a student’s score based on various input features like study hours, previous scores, and other factors.

**It includes:**  
Data preprocessing  
Model training  
API development using FastAPI  
Deployment (Render)  
Prediction logging using SQLite  

**Live Demo**  
👉 https://student-score-prediction-end-end-ml-wy13.onrender.com/

👉 API Docs (Swagger UI):  
👉 https://student-score-prediction-end-end-ml-wy13.onrender.com/docs

**Tech Stack**  
Python  
FastAPI  
Scikit-learn  
Pandas / NumPy  
SQLite  
Joblib  
Render (Deployment)  

**Project structure:**  
📁database.ipynb       #Model training script  
📁student_fastapi.py   #FastAPI app  
📁student_model.pkl    #Trained ML model  
📁student_scaler.pkl   #scaler-preprocesing  
📁predictions.db       #SQLite database  
📁requirement.txt      #required libraries 

**Model Details**  
Algorithm: Linear Regression Model  
Features used:  
Study Hours  
Sleep hours  
Previous Scores  
Target: Final score  

Sample Input
{
  "hours_studied": 5,
  "sleep_hours":7
  "previous_score": 70,
}
Sample Output
{
  "predicted_score": 78.5,
}
