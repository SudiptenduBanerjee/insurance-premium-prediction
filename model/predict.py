import pickle
import pandas as pd
from typing import Any, Dict


#import the ml model
with open('/home/sea-dragon/insurence-premium-prediction/model/model.pkl', 'rb') as f:
    model = pickle.load(f)


MODEL_VERSION = "1.0.0"


def predict_output(user_input: Dict[str, Any]):
    input_df = pd.DataFrame(user_input)
    

    output = model.predict(input_df)[0]
    return output