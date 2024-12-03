from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.resume_parser import parse_resume
from utils.gemini_analyzer import analyze_resume
from utils.linkedin_scraper import search_jobs
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
if os.environ.get('FLASK_ENV') == 'production':
    # In production, only allow requests from your Netlify domain
    CORS(app, resources={
        r"/*": {
            "origins": [
                "https://your-netlify-app.netlify.app",  # Replace with your Netlify domain
                "http://localhost:3000"  # Keep local development working
            ],
            "methods": ["OPTIONS", "GET", "POST"],
            "allow_headers": ["Content-Type"]
        }
    })
else:
    # In development, allow all origins
    CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        logger.debug("Received analyze request")
        
        if 'file' not in request.files:
            logger.error("No file in request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({"error": "No file selected"}), 400
            
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            logger.error("Invalid file format")
            return jsonify({"error": "Invalid file format. Please upload a PDF or DOCX file"}), 400

        location = request.form.get('location', '').strip()
        
        logger.debug(f"Processing file: {file.filename}, Location: {location}")
        
        # Parse resume
        resume_text = parse_resume(file)
        if not resume_text:
            logger.error("Could not extract text from resume")
            return jsonify({"error": "Could not extract text from the resume"}), 400

        # Analyze with Gemini
        analysis = analyze_resume(resume_text)
        if not analysis:
            logger.error("Could not analyze resume with Gemini")
            return jsonify({"error": "Could not analyze the resume"}), 500

        # Search for jobs if location is provided
        if location:
            jobs = search_jobs(analysis['skills'], location)
            if jobs:
                analysis['recommended_roles'] = jobs

        logger.debug("Analysis completed successfully")
        return jsonify(analysis)

    except Exception as e:
        logger.error(f"Unexpected error in analyze: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
