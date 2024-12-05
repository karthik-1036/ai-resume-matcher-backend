import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        recommended_roles = []
        
        # Create individual job searches for top skills
        for skill in skills[:5]:  # Use top 5 skills
            # Basic URL encoding for the skill
            encoded_skill = quote_plus(skill.strip())
            base_url = "https://www.linkedin.com/jobs/search/?keywords="
            
            # Create the search URL
            url = base_url + encoded_skill
            if location and location.strip():
                encoded_location = quote_plus(location.strip())
                url += f"&location={encoded_location}"
            
            # Add the role to recommendations
            recommended_roles.append({
                "title": f"{skill} Jobs",
                "reason": f"Matching your {skill} skill",
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
                "title": "Software Development Jobs",
                "reason": "General technology positions",
                "link": default_url
            })
        
        logger.info(f"Generated {len(recommended_roles)} job recommendations")
        return recommended_roles

    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        # Return a default recommendation if something goes wrong
        return [{
            "title": "Software Development Jobs",
            "reason": "General technology positions",
            "link": "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
        }]
