# FashionOntoAI - Fashion Feature Extraction System

An AI-powered fashion feature extraction system with ontology management and multi-modal processing capabilities, developed for Stylumia NXT Hackathon 2024.

## Project Overview

FashionOntoAI is an intelligent system that combines computer vision, natural language processing, and ontology management to analyze fashion items and extract meaningful features. The system provides a user-friendly interface for managing fashion ontologies, extracting features from images, and collecting user feedback for continuous improvement.

## Features

- 🎯 **Ontology Management**: Visual interface to manage fashion-related terms and relationships
- 🖼️ **Feature Extraction**: AI-powered extraction of features from fashion images
- 📊 **Multi-modal Processing**: Combines vision and text analysis
- 🔄 **Feedback System**: Continuous learning through user feedback
- 🎨 **Responsive UI**: Dark/Light mode support with Bootstrap

## Architecture

### Directory Structure
```
FashionOntoAI/
├── static/              # Static assets
│   └── js/             # JavaScript files
│       ├── main.js     # Core functionality
│       ├── extraction.js    # Feature extraction
│       ├── feedback.js      # Feedback system
│       └── ontology.js      # Ontology visualization
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── extraction.html # Feature extraction page
│   ├── feedback.html   # Feedback interface
│   └── ontology.html   # Ontology management
├── utils/              # Utility modules
│   ├── image_processor.py   # Image analysis
│   ├── nlp_processor.py     # Text processing
│   └── ontology_manager.py  # Ontology operations
├── routes.py           # API endpoints
├── models.py           # Database models
├── database.py         # Database config
└── main.py            # Entry point
```

### System Architecture Flow
```
┌─────────────────┐         ┌──────────────────┐
│    Web Interface│         │Feature Extraction │
│  (HTML/JS/CSS)  │◄───────►│     Engine       │
└─────────────────┘         └──────────────────┘
         ▲                           ▲
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌──────────────────┐
│    Flask API    │         │  Image Processor  │
│    Backend      │◄───────►│  NLP Processor   │
└─────────────────┘         └──────────────────┘
         ▲                           ▲
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌──────────────────┐
│   PostgreSQL    │         │    Ontology      │
│   Database      │◄───────►│    Manager       │
└─────────────────┘         └──────────────────┘
         ▲                           ▲
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌──────────────────┐
│    Feedback     │         │   Continuous     │
│    System       │◄───────►│   Learning      │
└─────────────────┘         └──────────────────┘
```

### Key Components

1. **Web Interface**
   - Modern responsive UI with Bootstrap
   - Dark/Light theme support
   - Interactive ontology visualization
   - Real-time feature extraction

2. **Feature Extraction Engine**
   - Multi-modal processing
   - Computer vision analysis
   - Natural language processing
   - Pattern recognition

3. **Database Layer**
   - PostgreSQL for data persistence
   - Stores ontology relationships
   - Manages user feedback
   - Tracks extraction history

4. **Feedback System**
   - User feedback collection
   - Quality assessment
   - Continuous improvement
   - Performance metrics

5. **Ontology Management**
   - Fashion term hierarchy
   - Relationship mapping
   - Dynamic updates
   - Visual navigation

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fashiononto-ai
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

Required packages:
- flask
- flask-sqlalchemy
- flask-migrate
- sqlalchemy
- psycopg2-binary
- opencv-python
- python-dotenv
- opencv-python-headless
- numpy
- openai

3. Set up environment variables:
Create a `.env` file with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Team

- Team Name: Tech_Revenger
- Developer: Prasannaram

## Contributing

This project was developed as part of the Stylumia NXT Hackathon 2024. For further development:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
