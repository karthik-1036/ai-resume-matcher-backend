import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_linkedin_search_url(job_title, location=None):
    """Generate a LinkedIn job search URL with job title and optional location"""
    try:
        # Clean job title and encode for URL
        job_title = job_title.strip()
        encoded_title = quote_plus(job_title)
        
        # Start with basic search URL
        url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_title}"
        
        # Add location if provided
        if location and location.strip():
            encoded_location = quote_plus(location.strip())
            url += f"&location={encoded_location}"
            
        logger.debug(f"Generated LinkedIn URL: {url}")
        return url
    except Exception as e:
        logger.error(f"Error generating LinkedIn URL: {str(e)}")
        return ""

def scrape_linkedin_jobs(analysis_result, location=None):
    """Generate LinkedIn job search links based on the resume analysis and location preference"""
    try:
        logger.debug(f"Generating LinkedIn job links from analysis for location: {location}")
        
        if 'recommended_roles' in analysis_result:
            for role in analysis_result['recommended_roles']:
                job_title = role['title']
                job_link = get_linkedin_search_url(job_title, location)
                role['link'] = job_link
            return analysis_result['recommended_roles']
        
        logger.debug("No recommended roles found in analysis")
        return []
        
    except Exception as e:
        logger.error(f"Error generating LinkedIn job links: {str(e)}")
        return []
