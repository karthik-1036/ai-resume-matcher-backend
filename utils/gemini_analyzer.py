import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure the Gemini API
genai.configure(api_key=api_key)

def analyze_resume(resume_text):
    """
    Analyze resume text using Google's Gemini API
    Returns extracted skills and recommended roles
    """
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-pro')
        logger.debug("Gemini model initialized")
        
        # Craft the prompt for Gemini
        prompt = f"""
        You are an expert career counselor and resume analyzer. Carefully analyze this resume and provide EXACTLY:

        1. TOP 5 MOST IMPORTANT SKILLS ONLY - Combine both technical and professional skills
        2. Experience Level - Based on years and role complexity
        3. Exactly 5 recommended job roles that best match their skills

        Format your response as a valid JSON object with this EXACT structure:
        {{
            "skills": [
                "skill1",  // List EXACTLY 5 most important skills
                "skill2",
                "skill3",
                "skill4",
                "skill5"
            ],
            "experience_level": "entry/mid/senior",
            "recommended_roles": [
                {{
                    "title": "Common LinkedIn Job Title",
                    "reason": "Clear explanation why this role matches their skills and experience"
                }},
                ... // Exactly 5 roles
            ]
        }}

        Guidelines:
        1. Skills (EXACTLY 5):
           - Choose the 5 most valuable and relevant skills
           - Mix of technical and soft skills
           - List in order of importance
           - Be specific (e.g., "Python" instead of just "Programming")

        2. Experience Level:
           - Entry (0-2 years): Recent grads, junior roles
           - Mid (3-5 years): Independent work, team lead
           - Senior (5+ years): Strategic decisions, management

        3. Job Roles (EXACTLY 5):
           - Use ONLY common job titles that are frequently posted on LinkedIn
           - Examples of common titles:
             * Software Engineer
             * Data Analyst
             * Product Manager
             * Full Stack Developer
             * Frontend Developer
             * Backend Developer
             * DevOps Engineer
             * Business Analyst
             * Project Manager
             * Sales Manager
             * Marketing Manager
             * Account Manager
             * Operations Manager
             * HR Manager
           - Avoid overly specific or uncommon titles
           - Match roles to candidate's skills and experience level
           - Focus on roles with high number of openings

        Resume to analyze:
        {resume_text}

        IMPORTANT:
        - MUST provide EXACTLY 5 skills
        - MUST provide EXACTLY 5 job roles
        - Use ONLY common job titles that frequently appear on LinkedIn
        - Ensure job titles match actual job postings
        - Keep explanations clear and concise

        Respond ONLY with the JSON object, no additional text.
        """

        logger.debug("Sending request to Gemini API...")
        response = model.generate_content(prompt)
        logger.debug("Received response from Gemini API")
        
        # Parse the response
        try:
            # Clean up the response text
            json_str = response.text.strip()
            
            # Remove any markdown code blocks
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0].strip()
            elif '```' in json_str:
                json_str = json_str.split('```')[1].strip()
            
            # Remove any trailing commas that might break JSON parsing
            json_str = re.sub(r',\s*}', '}', json_str)
            json_str = re.sub(r',\s*]', ']', json_str)
            
            # Parse the JSON
            analysis = json.loads(json_str)
            
            # Validate the structure
            if 'skills' not in analysis or 'experience_level' not in analysis or 'recommended_roles' not in analysis:
                raise ValueError("Missing required keys in analysis result")
            
            # Ensure exactly 5 skills
            if not isinstance(analysis['skills'], list) or len(analysis['skills']) != 5:
                logger.warning("Incorrect number of skills, adjusting to 5...")
                if isinstance(analysis['skills'], list):
                    if len(analysis['skills']) > 5:
                        analysis['skills'] = analysis['skills'][:5]
                    else:
                        while len(analysis['skills']) < 5:
                            analysis['skills'].append("General Skills")
                else:
                    analysis['skills'] = ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5"]
            
            # Ensure exactly 5 roles
            if not isinstance(analysis['recommended_roles'], list) or len(analysis['recommended_roles']) != 5:
                logger.warning("Incorrect number of roles, adjusting to 5...")
                if isinstance(analysis['recommended_roles'], list):
                    if len(analysis['recommended_roles']) > 5:
                        analysis['recommended_roles'] = analysis['recommended_roles'][:5]
                    else:
                        default_role = {
                            "title": "General Role",
                            "reason": "Based on your skills and experience"
                        }
                        while len(analysis['recommended_roles']) < 5:
                            analysis['recommended_roles'].append(default_role)
                else:
                    analysis['recommended_roles'] = [
                        {"title": "Role 1", "reason": "Based on skills"},
                        {"title": "Role 2", "reason": "Based on skills"},
                        {"title": "Role 3", "reason": "Based on skills"},
                        {"title": "Role 4", "reason": "Based on skills"},
                        {"title": "Role 5", "reason": "Based on skills"}
                    ]
            
            # Clean up and standardize the output
            analysis['skills'] = [str(skill).strip() for skill in analysis['skills']]
            analysis['experience_level'] = str(analysis['experience_level']).lower().strip()
            
            for role in analysis['recommended_roles']:
                if not isinstance(role, dict) or 'title' not in role or 'reason' not in role:
                    raise ValueError("Invalid role structure")
                role['title'] = str(role['title']).strip()
                role['reason'] = str(role['reason']).strip()
            
            logger.debug("Successfully validated analysis structure")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            logger.error(f"Raw response: {response.text}")
            raise Exception(f"Failed to parse response: {str(e)}")
        except ValueError as e:
            logger.error(f"Invalid analysis structure: {e}")
            raise Exception(f"Invalid analysis structure: {str(e)}")

    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise Exception(f"Error analyzing resume: {str(e)}")
