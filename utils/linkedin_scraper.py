import logging
from urllib.parse import quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_linkedin_search_url(query, location=None):
    """Generate a LinkedIn job search URL based on query and location"""
    try:
        # Clean and encode the search query
        encoded_query = quote_plus(query.strip())
        
        # Base LinkedIn jobs search URL
        url = "https://www.linkedin.com/jobs/search/?"
        
        # Add search parameters
        params = [f"keywords={encoded_query}"]
        
        # Add location if provided
        if location and location.strip():
            encoded_location = quote_plus(location.strip())
            params.append(f"location={encoded_location}")
        
        # Add additional parameters for better results
        params.extend([
            "f_TPR=r86400",  # Last 24 hours
            "position=1",
            "pageNum=0"
        ])
        
        # Combine URL with parameters
        final_url = url + "&".join(params)
        
        logger.info(f"Generated LinkedIn URL: {final_url}")
        return final_url
    except Exception as e:
        logger.error(f"Error generating LinkedIn URL: {str(e)}")
        return None

def search_jobs(skills, location=None):
    """Search for jobs based on skills and location"""
    try:
        recommended_roles = []
        
        # Create job searches based on top skills combinations
        if len(skills) >= 3:
            # Use top 3 skills together
            main_skills = " ".join(skills[:3])
            url = get_linkedin_search_url(main_skills, location)
            if url:
                recommended_roles.append({
                    "title": f"Jobs matching your top skills: {', '.join(skills[:3])}",
                    "reason": "Based on your primary skill combination",
                    "link": url
                })
        
        # Add individual searches for top skills
        for skill in skills[:3]:  # Use top 3 skills individually
            url = get_linkedin_search_url(skill, location)
            if url:
                recommended_roles.append({
                    "title": f"{skill} positions",
                    "reason": f"Based on your {skill} expertise",
                    "link": url
                })
        
        # If no roles were found, create a generic search
        if not recommended_roles:
            generic_query = "software developer"  # Default fallback search
            url = get_linkedin_search_url(generic_query, location)
            if url:
                recommended_roles.append({
                    "title": "Software Development Positions",
                    "reason": "General technology roles matching your profile",
                    "link": url
                })
        
        logger.info(f"Generated {len(recommended_roles)} job recommendations")
        return recommended_roles
    except Exception as e:
        logger.error(f"Error in job search: {str(e)}")
        return [
            {
                "title": "Software Development Jobs",
                "reason": "General technology positions",
                "link": "https://www.linkedin.com/jobs/search/?keywords=software%20developer"
            }
        ]  # Return fallback option
