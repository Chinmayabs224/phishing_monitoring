import joblib
import sys
import os

sys.path.append(os.path.abspath('.'))

try:
    model = joblib.load('models/phishing_model.pkl')
    print("Model loaded successfully.")
    if hasattr(model, 'feature_names_in_'):
        print("Features expected by model:")
        for f in model.feature_names_in_:
            print(f" - {f}")
    else:
        print("Model does not have feature_names_in_ attribute.")
except Exception as e:
    print(f"Error loading model: {e}")
