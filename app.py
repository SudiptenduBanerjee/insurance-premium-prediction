from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from schema.user_input import UserInput

#import the ml model
with open('/home/sea-dragon/insurence-premium-prediction/model/model.pkl', 'rb') as f:
    model = pickle.load(f)


MODEL_VERSION = "1.0.0"


# Initialize FastAPI app
app = FastAPI()

# Define the root endpoint
@app.get("/version")
def get_version():
    return {"version": MODEL_VERSION}


@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"message": "API is healthy"
            , "version": MODEL_VERSION
            , "status": "OK"
            }   


@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'lifestyle_risk': data.lifestyle_risk,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'occupation': data.occupation,
        'income_lpa': data.income_lpa
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={'predicted_category': prediction})