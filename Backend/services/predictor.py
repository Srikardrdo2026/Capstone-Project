import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "behavior_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "protocol_encoder.pkl")

model = joblib.load(MODEL_PATH)
protocol_encoder = joblib.load(ENCODER_PATH)

def predict_behavior(features):
    # Encode protocol safely
    try:
        encoded_protocol = protocol_encoder.transform([features["protocol"]])[0]
    except:
        encoded_protocol = 0

    # IMPORTANT: column names MUST match model training exactly
    data = pd.DataFrame([{
        "Login Hour": features["login_hour"],
        "Session Duration": features["session_duration"],
        "Commands": features["commands_count"],
        "Failed Logins": features["failed_logins"],
        "Typing Speed": features["typing_speed"]
    }])

    # Predict
    pred = model.predict(data)[0]
    conf = model.predict_proba(data)[0][pred]

    return {
        "prediction": int(pred),
        "confidence": round(float(conf), 3)
    }
