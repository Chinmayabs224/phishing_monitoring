import sys
import os
import pandas as pd
import joblib

# Add src to path
sys.path.append(os.path.abspath('.'))

from src.feature_extractor import URLFeatureExtractor

# Load model
try:
    model = joblib.load('models/phishing_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

extractor = URLFeatureExtractor()
url = "newgiftst.top"
features = extractor.extract_features(url)

print(f"URL: {url}")
print(f"Features: {features}")

# Predict
features_df = pd.DataFrame([features])
prediction = model.predict(features_df)[0]
proba = model.predict_proba(features_df)[0]

print(f"Prediction: {prediction} (0=Legitimate, 1=Phishing)")
print(f"Probabilities: {proba}")
