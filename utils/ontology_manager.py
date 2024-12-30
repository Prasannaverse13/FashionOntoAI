from app import db
from models import Ontology
from utils.nlp_processor import NLPProcessor

class OntologyManager:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
    
    def add_term(self, term_data):
        """
        Add a new term to the ontology
        """
        term = Ontology(
            term=term_data['term'],
            category=term_data['category'],
            parent_term=term_data.get('parent_term'),
            description=term_data.get('description')
        )
        db.session.add(term)
        db.session.commit()
        return term
    
    def get_term(self, term_id):
        """
        Retrieve a term by ID
        """
        return Ontology.query.get(term_id)
    
    def update_term(self, term_id, term_data):
        """
        Update an existing term
        """
        term = self.get_term(term_id)
        if term:
            term.term = term_data.get('term', term.term)
            term.category = term_data.get('category', term.category)
            term.parent_term = term_data.get('parent_term', term.parent_term)
            term.description = term_data.get('description', term.description)
            db.session.commit()
        return term
    
    def delete_term(self, term_id):
        """
        Delete a term from the ontology
        """
        term = self.get_term(term_id)
        if term:
            db.session.delete(term)
            db.session.commit()
            return True
        return False
    
    def search_terms(self, query):
        """
        Search for terms in the ontology
        """
        return Ontology.query.filter(
            Ontology.term.ilike(f'%{query}%')
        ).all()
    
    def get_hierarchy(self):
        """
        Get the complete ontology hierarchy
        """
        terms = Ontology.query.all()
        hierarchy = {}
        
        for term in terms:
            if not term.parent_term:
                hierarchy[term.term] = self._build_subtree(terms, term.term)
        
        return hierarchy
    
    def _build_subtree(self, terms, parent):
        """
        Build a subtree of terms under a parent
        """
        subtree = {}
        children = [t for t in terms if t.parent_term == parent]
        
        for child in children:
            subtree[child.term] = self._build_subtree(terms, child.term)
        
        return subtree
    
    def suggest_new_terms(self, text):
        """
        Suggest new terms based on text analysis
        """
        return self.nlp_processor.suggest_ontology_terms(text)
    
    def export_ontology(self):
        """
        Export the complete ontology as JSON
        """
        terms = Ontology.query.all()
        return {
            'terms': [
                {
                    'id': term.id,
                    'term': term.term,
                    'category': term.category,
                    'parent_term': term.parent_term,
                    'description': term.description
                }
                for term in terms
            ]
        }

    def _load_fashion_terms(self):
        """
        Load hierarchical fashion-specific terms and their categories
        """
        return {
            'apparel': {
                'tops': {
                    'categories': ['t-shirt', 'shirt', 'blouse', 'sweater', 'hoodie'],
                    'attributes': {
                        'sleeve_length': ['short', 'long', '3/4', 'sleeveless'],
                        'neckline': ['crew', 'v-neck', 'turtle', 'collared'],
                        'fit': ['regular', 'slim', 'oversized', 'fitted']
                    }
                },
                'bottoms': {
                    'categories': ['jeans', 'trousers', 'shorts', 'skirts'],
                    'attributes': {
                        'rise': ['high', 'mid', 'low'],
                        'length': ['full', 'cropped', 'ankle', 'mini', 'midi', 'maxi'],
                        'fit': ['skinny', 'straight', 'wide', 'bootcut']
                    }
                },
                'dresses': {
                    'categories': ['casual', 'formal', 'maxi', 'mini'],
                    'attributes': {
                        'silhouette': ['a-line', 'sheath', 'shift', 'wrap'],
                        'length': ['mini', 'midi', 'maxi', 'knee-length'],
                        'sleeve_type': ['sleeveless', 'cap', 'short', 'long']
                    }
                }
            },
            'materials': {
                'natural': ['cotton', 'silk', 'wool', 'linen', 'leather'],
                'synthetic': ['polyester', 'nylon', 'spandex', 'rayon'],
                'blends': ['cotton-polyester', 'wool-blend', 'silk-blend']
            },
            'patterns': {
                'geometric': ['striped', 'checked', 'polka dot', 'geometric'],
                'decorative': ['floral', 'paisley', 'abstract', 'animal'],
                'textures': ['plain', 'ribbed', 'quilted', 'embossed']
            },
            'styles': {
                'aesthetic': ['casual', 'formal', 'bohemian', 'vintage', 'modern'],
                'occasion': ['workwear', 'party', 'sportswear', 'loungewear'],
                'seasonal': ['summer', 'winter', 'spring', 'fall']
            },
            'colors': {
                'basic': ['black', 'white', 'gray', 'navy'],
                'primary': ['red', 'blue', 'yellow'],
                'secondary': ['green', 'purple', 'orange'],
                'neutral': ['beige', 'brown', 'khaki', 'cream']
            }
        }