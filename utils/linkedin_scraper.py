import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_linkedin_url(query, location=None):
    """Create a LinkedIn search URL with proper encoding"""
    try:
        # Ensure the query is a string and not empty
        if not query or not isinstance(query, (str, int, float)):
            return "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
            
        # Clean and encode the query
        cleaned_query = str(query).strip()
        if not cleaned_query:
            return "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
            
        # Create the base URL with encoded query
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(cleaned_query)}"
        
        # Add location if provided
        if location and str(location).strip():
            url += f"&location={quote_plus(str(location).strip())}"
            
        logger.info(f"Generated LinkedIn URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Error creating LinkedIn URL: {str(e)}")
        return "https://www.linkedin.com/jobs/search/?keywords=software%20developer"

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        # Ensure skills is a list of strings
        if isinstance(skills, str):
            skills = [skills]
        elif not isinstance(skills, list):
            logger.error(f"Invalid skills type: {type(skills)}")
            return get_default_role(location)
            
        # Clean and validate skills
        cleaned_skills = []
        for skill in skills:
            if skill and isinstance(skill, (str, int, float)):
                cleaned_skill = str(skill).strip()
                if cleaned_skill:
                    cleaned_skills.append(cleaned_skill)
        
        if not cleaned_skills:
            logger.warning("No valid skills provided")
            return get_default_role(location)
            
        recommended_roles = []
        
        # Create specialized role recommendations based on individual skills
        skill_role_mapping = {
            "python": {
                "title": "Python Developer",
                "description": "Design and implement high-quality Python applications",
                "requirements": ["Python expertise", "Software development experience", "Problem-solving skills"]
            },
            "javascript": {
                "title": "Frontend Developer",
                "description": "Create responsive and dynamic web applications",
                "requirements": ["JavaScript proficiency", "Frontend framework experience", "Web development skills"]
            },
            "react": {
                "title": "React Developer",
                "description": "Build modern user interfaces with React",
                "requirements": ["React.js expertise", "Frontend development skills", "State management experience"]
            },
            "node": {
                "title": "Backend Developer",
                "description": "Develop scalable backend services",
                "requirements": ["Node.js expertise", "API development", "Database management"]
            },
            "java": {
                "title": "Java Developer",
                "description": "Build enterprise-level Java applications",
                "requirements": ["Java expertise", "Spring Framework", "Enterprise software development"]
            },
            "sql": {
                "title": "Database Developer",
                "description": "Design and optimize database solutions",
                "requirements": ["SQL expertise", "Database design", "Performance optimization"]
            },
            "aws": {
                "title": "Cloud Engineer",
                "description": "Architect and implement cloud solutions",
                "requirements": ["AWS expertise", "Cloud architecture", "DevOps practices"]
            },
            "docker": {
                "title": "DevOps Engineer",
                "description": "Implement and maintain CI/CD pipelines",
                "requirements": ["Container orchestration", "Infrastructure as code", "Automation expertise"]
            }
        }
        
        # First, create a combined skills search for top 3 skills
        if len(cleaned_skills) >= 2:
            top_skills = cleaned_skills[:3]
            combined_query = " ".join(top_skills)
            url = create_linkedin_url(combined_query, location)
            
            role = {
                "title": "Senior Technology Professional",
                "reason": f"Based on your expertise in {', '.join(top_skills)}",
                "description": "This role combines your top technical skills, ideal for senior positions that require a diverse skill set.",
                "requirements": [f"Strong experience in {skill}" for skill in top_skills],
                "link": url
            }
            logger.info(f"Created combined skills role with URL: {url}")
            recommended_roles.append(role)
        
        # Add specialized roles based on individual skills
        for skill in cleaned_skills[:4]:  # Use top 4 skills
            skill_lower = skill.lower()
            url = create_linkedin_url(skill, location)
            
            if skill_lower in skill_role_mapping:
                role_template = skill_role_mapping[skill_lower]
                role = {
                    "title": role_template["title"],
                    "reason": f"Matches your {skill} expertise",
                    "description": role_template["description"],
                    "requirements": role_template["requirements"],
                    "link": url
                }
            else:
                role = {
                    "title": f"{skill} Specialist",
                    "reason": f"Based on your {skill} proficiency",
                    "description": f"Specialized role focusing on {skill} development and implementation",
                    "requirements": [
                        f"Strong {skill} expertise",
                        "Software development experience",
                        "Problem-solving abilities"
                    ],
                    "link": url
                }
            
            logger.info(f"Created role for {skill} with URL: {url}")
            recommended_roles.append(role)
        
        if not recommended_roles:
            logger.warning("No roles generated, returning default role")
            return get_default_role(location)
            
        logger.info(f"Successfully generated {len(recommended_roles)} job recommendations")
        return recommended_roles

    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        return get_default_role(location)

def get_default_role(location=None):
    """Return default role with proper URL"""
    url = create_linkedin_url("software developer", location)
    default_role = {
        "title": "Software Developer",
        "reason": "Based on your technical background",
        "description": "General software development role matching your technical skills",
        "requirements": [
            "Software development experience",
            "Programming proficiency",
            "Problem-solving abilities"
        ],
        "link": url
    }
    logger.info(f"Created default role with URL: {url}")
    return [default_role]
