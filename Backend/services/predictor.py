import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "behavior_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "protocol_encoder.pkl")

model = joblib.load(MODEL_PATH)
protocol_encoder = joblib.load(ENCODER_PATH)

def predict_behavior(features):
    try:
        encoded_protocol = protocol_encoder.transform([features["protocol"]])[0]
    except:
        encoded_protocol = 0

    data = pd.DataFrame([[ 
        features["login_hour"],
        features["session_duration"],
        features["commands_count"],
        features["failed_logins"],
        encoded_protocol,
        features["typing_speed"]
    ]], columns=[
        "LoginHour",
        "SessionDuration",
        "CommandsCount",
        "FailedLogins",
        "Protocol",
        "TypingSpeed"
    ])

    pred = model.predict(data)[0]
    conf = model.predict_proba(data)[0][pred]

    return {
        "prediction": int(pred),
        "confidence": round(conf, 3)
    }
