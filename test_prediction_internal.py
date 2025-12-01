import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.web.app import app

def test_prediction_endpoint():
    client = app.test_client()
    
    # Test Case 1: Legitimate URL
    payload_safe = {"url": "https://www.google.com"}
    print(f"\nTesting Safe URL: {payload_safe['url']}")
    response = client.post('/api/predict', json=payload_safe)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    if response.status_code != 200:
        raise Exception(f"Expected 200, got {response.status_code}")
    
    data = response.get_json()
    if 'is_phishing' not in data:
        raise Exception("Response missing 'is_phishing' field")
    if 'probability' not in data:
        raise Exception("Response missing 'probability' field")

    # Test Case 2: Phishing URL (Simulated)
    payload_phish = {"url": "http://192.168.1.1/login.php?user=admin"}
    print(f"\nTesting Phishing URL: {payload_phish['url']}")
    response = client.post('/api/predict', json=payload_phish)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    if response.status_code != 200:
        raise Exception(f"Expected 200, got {response.status_code}")
    
    data = response.get_json()
    if 'is_phishing' not in data:
        raise Exception("Response missing 'is_phishing' field")

if __name__ == "__main__":
    try:
        test_prediction_endpoint()
        print("\n✅ Verification Successful!")
    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        sys.exit(1)
