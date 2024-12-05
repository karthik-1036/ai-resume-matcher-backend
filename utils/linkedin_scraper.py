import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        recommended_roles = []
        
        # First, create a combined skills search
        if len(skills) >= 2:
            top_skills = skills[:3]  # Use top 3 skills
            combined_skills = " ".join(top_skills)
            encoded_skills = quote_plus(combined_skills)
            base_url = "https://www.linkedin.com/jobs/search/?keywords="
            
            url = base_url + encoded_skills
            if location and location.strip():
                encoded_location = quote_plus(location.strip())
                url += f"&location={encoded_location}"
            
            recommended_roles.append({
                "title": "Senior Technology Professional",
                "reason": f"Based on your expertise in {', '.join(top_skills)}",
                "description": "This role combines your top technical skills, ideal for senior positions that require a diverse skill set.",
                "requirements": [f"Strong experience in {skill}" for skill in top_skills],
                "link": url
            })
        
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
        
        # Add specialized roles based on skills
        for skill in skills[:4]:  # Use top 4 skills
            skill_lower = skill.lower()
            encoded_skill = quote_plus(skill)
            base_url = "https://www.linkedin.com/jobs/search/?keywords="
            
            url = base_url + encoded_skill
            if location and location.strip():
                encoded_location = quote_plus(location.strip())
                url += f"&location={encoded_location}"
            
            # Get role details from mapping or create generic one
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
        
        # If no roles were created, add a default one
        if not recommended_roles:
            default_url = "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
            if location and location.strip():
                encoded_location = quote_plus(location.strip())
                default_url += f"&location={encoded_location}"
            
            recommended_roles.append({
                "title": "Software Developer",
                "reason": "Based on your technical background",
                "description": "General software development role matching your technical skills",
                "requirements": [
                    "Software development experience",
                    "Programming proficiency",
                    "Problem-solving abilities"
                ],
                "link": default_url
            })
        
        logger.info(f"Generated {len(recommended_roles)} job recommendations")
        return recommended_roles

    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        # Return a default recommendation if something goes wrong
        return [{
            "title": "Software Developer",
            "reason": "Based on your technical background",
            "description": "General software development role matching your technical skills",
            "requirements": [
                "Software development experience",
                "Programming proficiency",
                "Problem-solving abilities"
            ],
            "link": "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
        }]
