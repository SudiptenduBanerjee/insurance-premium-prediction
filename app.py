from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output,MODEL_VERSION


# Initialize FastAPI app
app = FastAPI()


# Define the root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}


# Health check endpoint
from typing import Dict, Any

@app.get("/health")
def health_check() -> Dict[str, Any]:
    return {"message": "API is healthy"
            , "version": MODEL_VERSION
            , "status": "OK"
            }   



@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input: Dict[str, Any] = {
        'bmi': data.bmi,
        'lifestyle_risk': data.lifestyle_risk,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'occupation': data.occupation,
        'income_lpa': data.income_lpa
    }


    try:
        prediction = predict_output(user_input)
        return JSONResponse(content={"predicted_premium": prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})