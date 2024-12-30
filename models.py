from datetime import datetime
from database import db

class Ontology(db.Model):
    """Model for fashion ontology terms"""
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    parent_term = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'term': self.term,
            'category': self.category,
            'parent_term': self.parent_term,
            'description': self.description
        }

class ExtractedFeature(db.Model):
    """Model for extracted fashion features"""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100), nullable=False)
    feature_name = db.Column(db.String(100), nullable=False)
    feature_value = db.Column(db.String(200))
    confidence_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    feedback_entries = db.relationship('FeedbackEntry', backref='feature', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'feature_name': self.feature_name,
            'feature_value': self.feature_value,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat()
        }

class FeedbackEntry(db.Model):
    """Model for user feedback on extracted features"""
    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('extracted_feature.id'))
    corrected_value = db.Column(db.String(200))
    feedback_type = db.Column(db.String(50))
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'feature_id': self.feature_id,
            'corrected_value': self.corrected_value,
            'feedback_type': self.feedback_type,
            'comments': self.comments,
            'created_at': self.created_at.isoformat()
        }
