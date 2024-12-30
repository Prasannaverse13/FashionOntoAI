import logging
import logging
from flask import jsonify, request, render_template
from models import ExtractedFeature, FeedbackEntry, Ontology
from database import db
from utils.nlp_processor import NLPProcessor
from utils.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from utils.nlp_processor import NLPProcessor
from utils.image_processor import ImageProcessor

# Configure logging
logger = logging.getLogger(__name__)

# Initialize processors
image_processor = ImageProcessor()
import os
import json
import logging
from flask import render_template, request, jsonify, send_file
from utils.nlp_processor import NLPProcessor
from utils.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize processors
nlp_processor = NLPProcessor()
image_processor = ImageProcessor()

# File storage paths
DATA_DIR = "data"
ONTOLOGY_FILE = os.path.join(DATA_DIR, "ontology.json")
os.makedirs(DATA_DIR, exist_ok=True)

def init_routes(app):
    # Page Routes
    @app.route('/')
    def home():
        try:
            return render_template('home.html')
        except Exception as e:
            logger.error(f"Error rendering home page: {e}")
            return str(e), 500

    @app.route('/ontology')
    def ontology():
        try:
            return render_template('ontology.html')
        except Exception as e:
            logger.error(f"Error rendering ontology page: {e}")
            return str(e), 500

    @app.route('/extraction')
    def extraction():
        try:
            return render_template('extraction.html')
        except Exception as e:
            logger.error(f"Error rendering extraction page: {e}")
            return str(e), 500

    @app.route('/feedback')
    def feedback():
        try:
            return render_template('feedback.html')
        except Exception as e:
            logger.error(f"Error rendering feedback page: {e}")
            return str(e), 500

    # API Routes
    @app.route('/api/ontology', methods=['GET'])
    def get_ontology():
        try:
            if os.path.exists(ONTOLOGY_FILE):
                with open(ONTOLOGY_FILE, 'r') as f:
                    return jsonify(json.load(f))
            return jsonify({})
        except Exception as e:
            logger.error(f"Error getting ontology: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/ontology/terms', methods=['POST'])
    def add_term():
        try:
            data = request.json
            ontology = {}
            if os.path.exists(ONTOLOGY_FILE):
                with open(ONTOLOGY_FILE, 'r') as f:
                    ontology = json.load(f)
            
            # Add new term
            term_id = str(len(ontology.get('terms', [])) + 1)
            term_data = {
                'id': term_id,
                'term': data['term'],
                'category': data['category'],
                'parent_term': data.get('parent_term'),
                'description': data.get('description')
            }
            
            if 'terms' not in ontology:
                ontology['terms'] = []
            ontology['terms'].append(term_data)
            
            # Save updated ontology
            with open(ONTOLOGY_FILE, 'w') as f:
                json.dump(ontology, f, indent=2)
            
            return jsonify(term_data)
        except Exception as e:
            logger.error(f"Error adding term: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/extractions/recent', methods=['GET'])
    def get_recent_extractions():
        try:
            # Get recent feature extractions from the database
            recent_features = ExtractedFeature.query.order_by(
                ExtractedFeature.created_at.desc()
            ).limit(10).all()
            
            features = [{
                'id': feature.id,
                'product_id': feature.product_id,
                'feature_name': feature.feature_name,
                'feature_value': feature.feature_value,
                'confidence_score': feature.confidence_score
            } for feature in recent_features]
            
            return jsonify(features)
        except Exception as e:
            logger.error(f"Error getting recent extractions: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/features/<int:feature_id>', methods=['GET'])
    def get_feature(feature_id):
        try:
            feature = ExtractedFeature.query.get_or_404(feature_id)
            return jsonify({
                'id': feature.id,
                'product_id': feature.product_id,
                'feature_name': feature.feature_name,
                'feature_value': feature.feature_value,
                'confidence_score': feature.confidence_score
            })
        except Exception as e:
            logger.error(f"Error getting feature {feature_id}: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/feedback', methods=['POST'])
    def submit_feedback():
        try:
            data = request.get_json()
            feedback = FeedbackEntry(
                feature_id=data['feature_id'],
                corrected_value=data['corrected_value'],
                feedback_type=data['feedback_type']
            )
            db.session.add(feedback)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            return jsonify({'error': str(e)}), 500
    @app.route('/api/categories', methods=['GET', 'POST'])
    def categories():
        if request.method == 'GET':
            try:
                # Load fashion terms from NLP processor
                nlp = NLPProcessor()
                categories = nlp._load_fashion_terms()
                return jsonify(categories)
            except Exception as e:
                logger.error(f"Error getting categories: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        elif request.method == 'POST':
            try:
                data = request.json
                # Just return success for now
                return jsonify({'status': 'success', 'message': 'Category added'}), 200
            except Exception as e:
                logger.error(f"Error adding category: {str(e)}")
                return jsonify({'error': str(e)}), 500

    @app.route('/api/extract', methods=['POST'])
    def extract_features():
        try:
            if 'image_file' not in request.files:
                return jsonify({'error': 'No image file uploaded'}), 400
                
            image_file = request.files['image_file']
            if not image_file:
                return jsonify({'error': 'Empty file'}), 400
                
            image_data = image_file.read()
            
            # Get the selected category
            category = request.form.get('category')
            if not category:
                return jsonify({'error': 'Category not selected'}), 400
                
            # Extract visual features with the selected category
            visual_features = image_processor.detect_fashion_item(image_data, category)
            
            extracted_features = [
                {
                    'name': 'Category',
                    'value': category.title(),
                    'confidence': 1.0
                },
                {
                    'name': 'Colors',
                    'value': ', '.join(visual_features['colors'][:3]),
                    'confidence': visual_features['confidence_score']
                },
                {
                    'name': 'Pattern',
                    'value': visual_features['pattern'],
                    'confidence': visual_features['confidence_score']
                }
            ]
            
            return jsonify({'features': extracted_features})
        except Exception as e:
            logger.error(f"Error in feature extraction: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return app
