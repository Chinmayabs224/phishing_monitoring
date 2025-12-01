import requests
import json

# Test URL prediction
url_to_test = "newgiftst.top"

# Add http:// if not present
if not url_to_test.startswith(('http://', 'https://')):
    url_to_test = 'http://' + url_to_test

print(f"Testing URL: {url_to_test}")

# Send request to Flask API
response = requests.post('http://localhost:5000/api/predict', 
                        json={'url': url_to_test})

if response.status_code == 200:
    result = response.json()
    print(f"\n✓ Prediction successful!")
    print(f"  URL: {result['url']}")
    print(f"  Is Phishing: {result['is_phishing']}")
    print(f"  Probability: {result['probability']:.2%}")
    print(f"\n  Features extracted:")
    for feature, value in result['features'].items():
        print(f"    - {feature}: {value}")
else:
    print(f"\n✗ Error: {response.status_code}")
    print(f"  {response.text}")
