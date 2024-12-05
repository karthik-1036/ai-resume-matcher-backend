import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        # Ensure skills is a list of strings and clean them
        if isinstance(skills, str):
            skills = [skills]
        
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
            
            recommended_roles.append({
                "title": "Senior Technology Professional",
                "reason": f"Based on your expertise in {', '.join(top_skills)}",
                "description": "This role combines your top technical skills, ideal for senior positions that require a diverse skill set.",
                "requirements": [f"Strong experience in {skill}" for skill in top_skills],
                "link": url
            })
        
        # Add specialized roles based on individual skills
        for skill in cleaned_skills[:4]:  # Use top 4 skills
            skill_lower = skill.lower()
            url = create_linkedin_url(skill, location)
            
            if skill_lower in skill_role_mapping:
                role = skill_role_mapping[skill_lower]
                recommended_roles.append({
                    "title": role["title"],
                    "reason": f"Matches your {skill} expertise",
                    "description": role["description"],
                    "requirements": role["requirements"],
                    "link": url
                })
            else:
                recommended_roles.append({
                    "title": f"{skill} Specialist",
                    "reason": f"Based on your {skill} proficiency",
                    "description": f"Specialized role focusing on {skill} development and implementation",
                    "requirements": [
                        f"Strong {skill} expertise",
                        "Software development experience",
                        "Problem-solving abilities"
                    ],
                    "link": url
                })
            
            logger.info(f"Created job search URL for {skill}")
        
        return recommended_roles if recommended_roles else get_default_role(location)

    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        return get_default_role(location)

def create_linkedin_url(query, location=None):
    """Create a LinkedIn search URL with proper encoding"""
    try:
        base_url = "https://www.linkedin.com/jobs/search/?"
        params = [f"keywords={quote_plus(str(query).strip())}"]
        
        if location and str(location).strip():
            params.append(f"location={quote_plus(str(location).strip())}")
        
        return base_url + "&".join(params)
    except Exception as e:
        logger.error(f"Error creating LinkedIn URL: {str(e)}")
        return "https://www.linkedin.com/jobs/search/?keywords=software%20developer"

def get_default_role(location=None):
    """Return default role with proper URL"""
    url = create_linkedin_url("software developer", location)
    return [{
        "title": "Software Developer",
        "reason": "Based on your technical background",
        "description": "General software development role matching your technical skills",
        "requirements": [
            "Software development experience",
            "Programming proficiency",
            "Problem-solving abilities"
        ],
        "link": url
    }]
