import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency

class DriftDetector:
    def __init__(self, reference_data):
        """
        Args:
            reference_data (pd.DataFrame): The training data to compare against.
        """
        self.reference_data = reference_data
        self.p_value_threshold = 0.05

    def detect_drift(self, new_data):
        """
        Checks for drift between reference_data and new_data.
        Returns a dictionary with drift status for each feature.
        """
        report = {}
        drift_detected = False
        
        # Identify features present in both datasets
        common_features = [col for col in self.reference_data.columns if col in new_data.columns]
        
        # Numerical features: Use Kolmogorov-Smirnov (KS) Test
        numerical_features = [
            'url_length', 'num_special_chars', 'domain_entropy', 
            'vowel_consonant_ratio', 'digit_count', 'subdomain_count'
        ]
        
        # Categorical features: Use Chi-Square Test
        categorical_features = [
            'has_ip_address', 'https_token', 'is_suspicious_tld', 'has_suspicious_keyword'
        ]

        for feature in common_features:
            try:
                if feature in numerical_features:
                    ref_values = self.reference_data[feature]
                    new_values = new_data[feature]
                    
                    # KS Test
                    statistic, p_value = ks_2samp(ref_values, new_values)
                    test_name = 'KS'
                    
                elif feature in categorical_features:
                    # Create contingency table
                    ref_counts = self.reference_data[feature].value_counts().sort_index()
                    new_counts = new_data[feature].value_counts().sort_index()
                    
                    # Align indexes
                    all_categories = sorted(list(set(ref_counts.index) | set(new_counts.index)))
                    ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
                    new_freq = [new_counts.get(cat, 0) for cat in all_categories]
                    
                    contingency_table = np.array([ref_freq, new_freq])
                    
                    # Remove columns with zero sum
                    contingency_table = contingency_table[:, contingency_table.sum(axis=0) > 0]

                    if contingency_table.shape[1] < 2:
                        p_value = 1.0
                    else:
                        chi2, p, dof, ex = chi2_contingency(contingency_table)
                        p_value = p
                    test_name = 'Chi-Square'
                else:
                    continue # Skip unknown features

                is_drift = p_value < self.p_value_threshold
                report[feature] = {
                    'test': test_name,
                    'p_value': float(p_value), # Ensure it's a float for JSON serialization
                    'drift_detected': bool(is_drift)
                }
                if is_drift:
                    drift_detected = True
                    
            except Exception as e:
                print(f"Error checking drift for {feature}: {e}")
                report[feature] = {
                    'test': 'Error',
                    'p_value': 1.0,
                    'drift_detected': False,
                    'error': str(e)
                }
                
        return drift_detected, report
