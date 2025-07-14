import streamlit as st
import requests
from typing import Dict, Any

# FastAPI endpoint
API_URL = "http://localhost:8000/predict"

# Streamlit app title and description
st.title("Insurance Premium Prediction")
st.write("Enter the details below to predict the insurance premium.")

# Create a form for user input
with st.form(key="user_input_form"):
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=119,
        value=30,
        step=1,
        help="Enter your age (1-119)"
    )
    
    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=70.0,
        step=0.1,
        help="Enter your weight in kilograms"
    )
    
    height = st.number_input(
        "Height (m)",
        min_value=0.1,
        max_value=2.5,
        value=1.7,
        step=0.01,
        help="Enter your height in meters (up to 2.5m)"
    )
    
    income_lpa = st.number_input(
        "Income (Lakhs per Annum)",
        min_value=0.1,
        value=5.0,
        step=0.1,
        help="Enter your annual income in lakhs"
    )
    
    smoker = st.selectbox(
        "Smoker",
        options=["Yes", "No"],
        help="Check if you are a smoke or not "
    )
    
    city = st.text_input(
        "City",
        value="Mumbai",
        help="Enter your city (e.g., Mumbai, Delhi)"
    )
    
    occupation = st.selectbox(
        "Occupation",
        options=[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ],
        help="Select your occupation"
    )
    
    # Submit button
    submit_button = st.form_submit_button(label="Predict Premium")

# Handle form submission
if submit_button:
    # Prepare the payload for the API request
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }
    
    try:
        # Make POST request to the FastAPI predict endpoint
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Extract predicted_premium and ensure it's a number
            predicted_premium = result.get("predicted_premium")
            if isinstance(predicted_premium, dict):
                predicted_premium_dict: Dict[str, Any] = predicted_premium
                category: str = str(predicted_premium_dict.get("predicted_category", "Unknown"))
                confidence_val = predicted_premium_dict.get("confidence", 0.0)
                if isinstance(confidence_val, (int, float)):
                    confidence = float(confidence_val)
                else:
                    confidence = 0.0
                class_probs = predicted_premium_dict.get("class_probabilities", {})
                if not isinstance(class_probs, dict):
                    class_probs = {}
                st.success(f"Predicted Category: {category} (Confidence: {confidence:.2f})")
            else:
                st.error(f"Error: Unexpected format for predicted_premium: {predicted_premium}")
        else:
            error_message = response.json().get("error", "Unknown error")
            st.error(f"API Error: {error_message}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the API: {str(e)}")