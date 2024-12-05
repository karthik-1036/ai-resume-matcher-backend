from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.resume_parser import parse_resume
from utils.gemini_analyzer import analyze_resume
from utils.linkedin_scraper import search_jobs
import os
from dotenv import load_dotenv
import logging
import time

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS - Allow all origins in production for testing
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Set timeouts for external API calls
GEMINI_TIMEOUT = 90  # seconds
LINKEDIN_TIMEOUT = 30  # seconds

@app.route('/analyze', methods=['POST'])
def analyze():
    start_time = time.time()
    try:
        logger.info("Received analyze request")
        logger.debug(f"Request headers: {dict(request.headers)}")
        logger.debug(f"Request form data: {dict(request.form)}")
        
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

        # Check file size (5MB limit)
        file_content = file.read()
        file.seek(0)  # Reset file pointer after reading
        if len(file_content) > 5 * 1024 * 1024:  # 5MB in bytes
            logger.error("File too large")
            return jsonify({"error": "File size too large. Please upload a file smaller than 5MB"}), 400

        location = request.form.get('location', '').strip()
        logger.info(f"Processing file: {file.filename}, Location: {location}")
        
        # Parse resume
        try:
            resume_text = parse_resume(file)
            if not resume_text:
                logger.error("Could not extract text from resume")
                return jsonify({"error": "Could not extract text from the resume"}), 400
            logger.info("Resume parsed successfully")
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            return jsonify({"error": f"Error parsing resume: {str(e)}"}), 500

        # Analyze with Gemini
        try:
            analysis = analyze_resume(resume_text)
            if not analysis or 'skills' not in analysis:
                logger.error("Invalid analysis result from Gemini")
                return jsonify({"error": "Could not analyze the resume properly"}), 500
            logger.info("Resume analyzed successfully with Gemini")
        except Exception as e:
            logger.error(f"Error analyzing resume with Gemini: {str(e)}")
            return jsonify({"error": f"Error analyzing resume: {str(e)}"}), 500

        # Search for jobs if location is provided
        if location and 'skills' in analysis:
            try:
                jobs = search_jobs(analysis['skills'], location)
                if jobs:
                    analysis['recommended_roles'] = jobs
                logger.info("Job search completed successfully")
            except Exception as e:
                logger.error(f"Error searching jobs: {str(e)}")
                analysis['recommended_roles'] = []

        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"Analysis completed successfully in {processing_time:.2f} seconds")
        
        return jsonify(analysis)

    except Exception as e:
        logger.error(f"Unexpected error in analyze: {str(e)}")
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": str(e),
            "processing_time": time.time() - start_time
        }), 500

# Error handling
@app.errorhandler(500)
def handle_500_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.errorhandler(502)
def handle_502_error(e):
    logger.error(f"Bad gateway error: {str(e)}")
    return jsonify({"error": "Bad gateway error", "message": str(e)}), 502

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
