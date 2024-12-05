import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_linkedin_search_url(skills, location=None):
    """Generate a LinkedIn job search URL based on skills and location"""
    try:
        # Join skills with OR for broader search
        search_query = " OR ".join(skills[:3])  # Use top 3 skills
        encoded_query = quote_plus(search_query)
        
        # Start with basic search URL
        url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}"
        
        # Add location if provided
        if location and location.strip():
            encoded_location = quote_plus(location.strip())
            url += f"&location={encoded_location}"
            
        logger.info(f"Generated LinkedIn URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Error generating LinkedIn URL: {str(e)}")
        return None

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        # Generate search URL
        url = get_linkedin_search_url(skills, location)
        if not url:
            return []

        # For now, return a list of recommended roles with the search URL
        recommended_roles = [
            {
                "title": f"Jobs matching {', '.join(skills[:3])}",
                "reason": "Based on your top skills",
                "link": url
            }
        ]
        
        logger.info(f"Generated {len(recommended_roles)} job recommendations")
        return recommended_roles
    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        return []
