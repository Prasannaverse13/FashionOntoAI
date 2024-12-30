import re
from collections import defaultdict

class NLPProcessor:
    def __init__(self):
        self.fashion_terms = self._load_fashion_terms()
    
    def _load_fashion_terms(self):
        """
        Load fashion-specific terms and their categories
        """
        return {
            'materials': ['cotton', 'silk', 'wool', 'polyester', 'leather', 'denim', 'linen'],
            'patterns': ['striped', 'floral', 'checked', 'polka dot', 'plain', 'geometric'],
            'styles': ['casual', 'formal', 'bohemian', 'vintage', 'modern', 'classic'],
            'features': ['sleeve', 'collar', 'neck', 'hem', 'waist', 'button', 'zip'],
            'colors': ['red', 'blue', 'green', 'yellow', 'black', 'white', 'purple',
                      'pink', 'orange', 'brown', 'gray', 'navy', 'beige', 'maroon']
        }
    
    def extract_features(self, text):
        """
        Extract fashion-relevant features from text description
        """
        text = text.lower()
        features = defaultdict(list)
        
        # Extract terms for each category
        for category, terms in self.fashion_terms.items():
            for term in terms:
                if term in text:
                    features[category].append(term)
        
        # Extract measurements
        measurements = re.findall(r'\d+(?:\.\d+)?(?:\s*(?:cm|mm|inch|"|\'|meters?))?', text)
        if measurements:
            features['measurements'] = measurements
        
        return dict(features)
    
    def suggest_ontology_terms(self, text):
        """
        Suggest new terms for the ontology based on text analysis
        """
        text = text.lower()
        words = text.split()
        suggestions = []
        
        for word in words:
            for category, terms in self.fashion_terms.items():
                if any(term in word for term in terms):
                    suggestions.append({
                        'term': word,
                        'category': category
                    })
        
        return suggestions
    
    def analyze_description(self, text):
        """
        Analyze product description and extract structured information
        """
        features = self.extract_features(text)
        potential_terms = self.suggest_ontology_terms(text)
        
        return {
            'extracted_features': features,
            'suggested_terms': potential_terms,
            'analysis': {
                'word_count': len(text.split()),
                'contains_measurements': bool(features.get('measurements')),
                'identified_categories': list(features.keys())
            }
        }