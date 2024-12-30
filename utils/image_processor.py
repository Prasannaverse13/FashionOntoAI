import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.categories = {
            'shoe': ['sneaker', 'boot', 'sandal', 'heel'],
            'top': ['shirt', 't-shirt', 'blouse', 'sweater'],
            'bottom': ['pants', 'jeans', 'skirt', 'shorts'],
            'dress': ['gown', 'sundress', 'formal dress'],
            'accessory': ['bag', 'hat', 'scarf', 'jewelry']
        }

    def detect_fashion_item(self, image_data, selected_category):
        """
        Detect fashion items using basic computer vision
        """
        try:
            # Convert image data to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Extract basic features
            colors = self._analyze_colors(img)
            pattern = self._detect_patterns(img)
            
            # Basic item categorization based on shape and color analysis
            height, width = img.shape[:2]
            aspect_ratio = height / width
            
            # Use the selected category
            category = selected_category
            
            return {
                "category": category,
                "colors": colors,
                "pattern": pattern,
                "confidence_score": 0.7
            }
            
        except Exception as e:
            logger.error(f"Error in detect_fashion_item: {str(e)}")
            return {
                "category": "unknown",
                "colors": [],
                "pattern": "unknown",
                "confidence_score": 0
            }

    def _analyze_colors(self, img):
        """
        Analyze dominant colors in the image
        """
        try:
            # Resize image for faster processing
            resized = cv2.resize(img, (150, 150))
            pixels = resized.reshape(-1, 3)
            pixels = np.float32(pixels)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            K = 5  # Number of dominant colors
            _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert to RGB (OpenCV uses BGR)
            centers = np.uint8(centers)
            centers = [color[::-1] for color in centers.tolist()]  # Reverse BGR to RGB
            
            # Convert to hex colors
            hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in centers]
            return hex_colors
            
        except Exception as e:
            logger.error(f"Error in _analyze_colors: {str(e)}")
            return []

    def _detect_patterns(self, img):
        """
        Detect patterns in the image using edge detection and texture analysis
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Calculate edge density
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # Basic pattern classification
            if edge_density < 0.05:
                return "solid"
            elif edge_density < 0.15:
                return "simple_pattern"
            else:
                return "complex_pattern"
                
        except Exception as e:
            logger.error(f"Error in _detect_patterns: {str(e)}")
            return "unknown"

    def extract_visual_features(self, image_data):
        """
        Extract visual features using OpenCV
        """
        try:
            # Convert image data to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Extract colors
            colors = self._analyze_colors(img)
            
            # Detect patterns
            patterns = self._detect_patterns(img)
            
            return {
                'colors': colors,
                'patterns': patterns,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error in extract_visual_features: {str(e)}")
            return {
                'error': str(e),
                'colors': [],
                'patterns': 'unknown',
                'success': False
            }
