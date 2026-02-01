import pandas as pd
import random
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

random.seed(42)
np.random.seed(42)

protocols = ["HTTPS", "SSH", "FTP", "TOR"]
data = []

for _ in range(1800):

    # Hidden intent
    intent = 1 if random.random() < 0.45 else 0  # 45% suspicious

    if intent == 1:
        login_hour = random.choice(list(range(0,6)) + list(range(22,24)))
        session_duration = random.randint(60, 220)
        commands_count = random.randint(15, 50)
        failed_logins = random.randint(1, 5)
        protocol = random.choices(protocols, weights=[2,2,1,3])[0]
        typing_speed = random.randint(60, 120)
    else:
        login_hour = random.randint(7, 21)
        session_duration = random.randint(10, 140)
        commands_count = random.randint(0, 35)
        failed_logins = random.randint(0, 3)
        protocol = random.choices(protocols, weights=[4,3,2,1])[0]
        typing_speed = random.randint(30, 90)

    # Observation noise (critical)
    if random.random() < 0.35:
        commands_count = random.randint(0, 50)
    if random.random() < 0.30:
        failed_logins = random.randint(0, 5)
    if random.random() < 0.30:
        typing_speed = random.randint(30, 120)
    if random.random() < 0.25:
        session_duration = random.randint(10, 220)

    # Label noise (REALISTIC)
    if random.random() < 0.20:
        intent = 1 - intent

    data.append([
        login_hour,
        session_duration,
        commands_count,
        failed_logins,
        protocol,
        typing_speed,
        intent
    ])

df = pd.DataFrame(data, columns=[
    "LoginHour",
    "SessionDuration",
    "CommandsCount",
    "FailedLogins",
    "Protocol",
    "TypingSpeed",
    "Label"
])

df.head()

df.to_csv("behavior_dataset.csv", index=False)
df["Label"].value_counts(normalize=True)
df_large = pd.concat([df] * 850, ignore_index=True)
df_large.to_csv("behavior_dataset_1M.csv", index=False)


encoder = LabelEncoder()
df["Protocol"] = encoder.fit_transform(df["Protocol"])

X = df[[
    "LoginHour", "SessionDuration", "CommandsCount",
    "FailedLogins", "Protocol", "TypingSpeed"
]]
y = df["Label"]

# HARDER test split (distribution shift)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=99
)

model = RandomForestClassifier(
    n_estimators=25,
    max_depth=3,
    min_samples_leaf=30,
    max_features=2,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)


joblib.dump(model, "behavior_model.pkl")
joblib.dump(encoder, "protocol_encoder.pkl")