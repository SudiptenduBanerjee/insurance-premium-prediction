import pickle
import pandas as pd
from typing import Any, Dict


#import the ml model
with open('/home/sea-dragon/insurence-premium-prediction/model/model.pkl', 'rb') as f:
    model = pickle.load(f)


MODEL_VERSION = "1.0.0"

class_labels = model.classes_.tolist()

def predict_output(user_input: Dict[str, Any]):
    df = pd.DataFrame([user_input])
    predicted_class = model.predict(df)[0]
    predicted_proba = model.predict_proba(df)[0].tolist()
    return {"predicted_class": class_labels[predicted_class], "predicted_proba": predicted_proba}