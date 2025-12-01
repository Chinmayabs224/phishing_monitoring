import requests
import json

# Test URLs
test_urls = [
    "rbwubtpsyokqn.info",  # Should be PHISHING (random chars + .info TLD)
    "newgiftst.top",        # Should be PHISHING (.top TLD)
    "https://www.google.com",  # Should be LEGITIMATE
    "https://www.amazon.com",  # Should be LEGITIMATE
]

print("=" * 70)
print("PHISHING DETECTION TEST - Enhanced Model with 10 Features")
print("=" * 70)

for url in test_urls:
    # Add http:// if not present
    test_url = url if url.startswith(('http://', 'https://')) else 'http://' + url
    
    print(f"\n{'─' * 70}")
    print(f"Testing: {url}")
    print(f"{'─' * 70}")
    
    # Send request to Flask API
    response = requests.post('http://localhost:5000/api/predict', 
                            json={'url': test_url})
    
    if response.status_code == 200:
        result = response.json()
        
        # Determine classification
        is_phishing = result['is_phishing']
        probability = result['probability']
        
        if is_phishing:
            status = f"⚠️  PHISHING ({probability:.1%} confidence)"
        else:
            status = f"✅ LEGITIMATE ({(1-probability):.1%} safe)"
        
        print(f"Result: {status}")
        print(f"\nKey Features:")
        features = result['features']
        print(f"  • Domain Entropy: {features.get('domain_entropy', 'N/A'):.2f}")
        print(f"  • Vowel Ratio: {features.get('vowel_consonant_ratio', 'N/A'):.2f}")
        print(f"  • Suspicious TLD: {'Yes' if features.get('is_suspicious_tld') else 'No'}")
        print(f"  • Suspicious Keyword: {'Yes' if features.get('has_suspicious_keyword') else 'No'}")
        print(f"  • Digit Count: {features.get('digit_count', 'N/A')}")
        print(f"  • Subdomain Count: {features.get('subdomain_count', 'N/A')}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"  {response.text}")

print(f"\n{'=' * 70}")
print("Test Complete!")
print(f"{'=' * 70}\n")
