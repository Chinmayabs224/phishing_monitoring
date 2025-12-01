import requests
import json

def test_prediction():
    url = "http://127.0.0.1:5000/api/predict"
    
    # Test Case 1: Legitimate URL
    payload_safe = {"url": "https://www.google.com"}
    try:
        response = requests.post(url, json=payload_safe)
        print(f"Testing Safe URL: {payload_safe['url']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing safe URL: {e}")

    print("-" * 20)

    # Test Case 2: Phishing URL (Simulated)
    payload_phish = {"url": "http://192.168.1.1/login.php?user=admin"}
    try:
        response = requests.post(url, json=payload_phish)
        print(f"Testing Phishing URL: {payload_phish['url']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing phishing URL: {e}")

if __name__ == "__main__":
    test_prediction()
