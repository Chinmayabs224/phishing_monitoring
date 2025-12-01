import re
import pandas as pd
import math
from urllib.parse import urlparse

class URLFeatureExtractor:
    """
    Extracts features from raw URLs for phishing detection.
    """
    
    def __init__(self):
        # Regex pattern to detect IP addresses in URLs
        self.ip_pattern = re.compile(
            r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
            r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
        )
        
        self.suspicious_tlds = ['.top', '.xyz', '.info', '.club', '.live', '.online', '.site', '.cn', '.ru']
        self.suspicious_keywords = ['login', 'secure', 'account', 'update', 'verify', 'signin', 'banking', 'confirm', 'wallet']
    
    def _calculate_entropy(self, text):
        """
        Calculate Shannon entropy of a string to detect randomness.
        Higher entropy = more random (suspicious).
        """
        if not text:
            return 0
        
        # Count character frequencies
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0
        text_len = len(text)
        for count in char_counts.values():
            probability = count / text_len
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _calculate_vowel_consonant_ratio(self, text):
        """
        Calculate ratio of vowels to total letters.
        Normal English words have ~40% vowels.
        Random strings often have unusual ratios.
        """
        if not text:
            return 0
        
        vowels = 'aeiouAEIOU'
        letters = [c for c in text if c.isalpha()]
        
        if not letters:
            return 0
        
        vowel_count = sum(1 for c in letters if c in vowels)
        return vowel_count / len(letters)
    
    def _count_digits(self, text):
        """Count number of digits in text."""
        return sum(1 for c in text if c.isdigit())
    
    def _count_subdomains(self, hostname):
        """
        Count number of subdomains.
        Example: secure.login.paypal.com has 3 subdomains
        """
        if not hostname:
            return 0
        
        # Remove port if present
        if ':' in hostname:
            hostname = hostname.split(':')[0]
        
        # Split by dots and count parts (minus the TLD and domain)
        parts = hostname.split('.')
        # Typical structure: [subdomain1, subdomain2, ..., domain, tld]
        # Count all parts except last 2 (domain + tld)
        return max(0, len(parts) - 2)
        
    def extract_features(self, url):
        """
        Extract features from a single URL.
        
        Returns:
            dict: Dictionary of features
        """
        features = {}
        
        # 1. URL Length
        features['url_length'] = len(url)
        
        # 2. Number of Special Characters
        special_chars = ['@', '-', '_', '.', '?', '=', '&', '!', '#', '%', '+', '$', ',', '//']
        features['num_special_chars'] = sum(url.count(char) for char in special_chars)
        
        # 3. Has IP Address
        features['has_ip_address'] = 1 if self.ip_pattern.search(url) else 0
        
        # 4. HTTPS Token
        features['https_token'] = 1 if url.startswith('https://') else 0
        
        # 5. Suspicious TLD
        parsed = urlparse(url)
        hostname = parsed.netloc if parsed.netloc else parsed.path
        if '/' in hostname:
            hostname = hostname.split('/')[0]
        features['is_suspicious_tld'] = 1 if any(hostname.endswith(tld) for tld in self.suspicious_tlds) else 0
        
        # 6. Suspicious Keywords
        features['has_suspicious_keyword'] = 1 if any(keyword in url.lower() for keyword in self.suspicious_keywords) else 0
        
        # 7. Domain Entropy (randomness detection)
        # Extract just the domain name (without TLD)
        domain_parts = hostname.split('.')
        if len(domain_parts) >= 2:
            domain_name = domain_parts[-2]  # Get domain without TLD
        else:
            domain_name = hostname
        features['domain_entropy'] = self._calculate_entropy(domain_name)
        
        # 8. Vowel-Consonant Ratio
        features['vowel_consonant_ratio'] = self._calculate_vowel_consonant_ratio(domain_name)
        
        # 9. Digit Count
        features['digit_count'] = self._count_digits(hostname)
        
        # 10. Subdomain Count
        features['subdomain_count'] = self._count_subdomains(hostname)
        
        return features
    
    def extract_features_batch(self, urls):
        """
        Extract features from a list of URLs.
        
        Args:
            urls: List of URL strings
            
        Returns:
            pd.DataFrame: DataFrame with extracted features
        """
        features_list = [self.extract_features(url) for url in urls]
        return pd.DataFrame(features_list)
    
    def process_dataset(self, csv_path, label_column='Label', url_column='URL', sample_size=None):
        """
        Load and process a phishing dataset CSV.
        
        Args:
            csv_path: Path to CSV file
            label_column: Name of the label column
            url_column: Name of the URL column
            sample_size: Optional number of rows to sample
            
        Returns:
            pd.DataFrame: DataFrame with features and labels
        """
        # Determine separator based on extension or content
        # For the user provided dataset, it uses ';'
        try:
            df = pd.read_csv(csv_path)
            if len(df.columns) < 2: # Likely wrong separator
                df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')
        except:
            df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')
            
        # Handle column renaming if needed for specific datasets
        if 'id' in df.columns and 'threat_status' in df.columns:
            url_column = 'id'
            label_column = 'threat_status'
        
        # Sample if requested
        if sample_size and sample_size < len(df):
            df = df.sample(n=sample_size, random_state=42)
        
        # Extract features
        features_df = self.extract_features_batch(df[url_column].values)
        
        # Convert labels
        # 'good'/'whitelist' -> 0
        # 'bad'/'malicious' -> 1
        if label_column in df.columns:
            labels = df[label_column].astype(str).str.lower().map({
                'good': 0, 'whitelist': 0, '0': 0,
                'bad': 1, 'malicious': 1, '1': 1
            })
            # Fill NaN if mapping failed for some rows
            labels = labels.fillna(0).astype(int)
            features_df['is_phishing'] = labels.values
        
        return features_df

if __name__ == "__main__":
    # Test with sample URLs
    extractor = URLFeatureExtractor()
    
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login",
        "http://suspicious-site-with-many-dashes-and-special-chars.com/login?user=admin&pass=123"
    ]
    
    for url in test_urls:
        features = extractor.extract_features(url)
        print(f"\nURL: {url}")
        print(f"Features: {features}")
