import sys
import os
sys.path.append(os.path.abspath('.'))

from src.feature_extractor import URLFeatureExtractor

# Test the suspicious URL
url = "rbwubtpsyokqn.info"
if not url.startswith(('http://', 'https://')):
    url = 'http://' + url

extractor = URLFeatureExtractor()
features = extractor.extract_features(url)

print(f"URL: {url}")
print(f"\nExtracted Features:")
for feature, value in features.items():
    print(f"  {feature}: {value}")

# Also test a clearly legitimate URL for comparison
legit_url = "https://www.google.com"
legit_features = extractor.extract_features(legit_url)

print(f"\n\nComparison - Legitimate URL: {legit_url}")
print(f"Extracted Features:")
for feature, value in legit_features.items():
    print(f"  {feature}: {value}")
