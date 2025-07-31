# site_finder.py (updated)
import time
import random
from urllib.parse import urlparse
from googlesearch import search

# Configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MentalHealthResourceFinder/1.0"
SEARCH_QUERY = "free mental health resources OR support OR hotline OR counseling -paid -advertisement"
NUM_RESULTS = 100
DELAY = random.uniform(1, 3)

# Trust indicators
TRUSTED_DOMAINS = ['.gov', '.edu', '.org', 'crisis', 'helpline', 'nami', 'samhsa']
POSITIVE_KEYWORDS = ['mental health', 'support', 'help', 'counseling', 'therapy']
NEGATIVE_KEYWORDS = ['paid', 'advertisement', 'sponsor', 'buy', 'purchase']

def is_good_site(url):
    """Determine if a site is likely a good resource based on URL only"""
    url_lower = url.lower()
    
    # Skip if any negative indicators
    if any(bad in url_lower for bad in NEGATIVE_KEYWORDS):
        return False
    
    # Check domain trust
    domain = urlparse(url).netloc.lower()
    if any(td in domain for td in TRUSTED_DOMAINS):
        return True
    
    # Check URL path
    good_url_indicators = ['/resources', '/help', '/support', 'mental-health']
    if any(indicator in url_lower for indicator in good_url_indicators):
        return True
    
    return False

def find_mental_health_sites():
    """Find potential mental health resource sites"""
    good_sites = []
    
    print(f"Searching Google for mental health resources...")
    
    try:
        # Perform Google search
        for url in search(
            SEARCH_QUERY,
            lang='en',
            stop=NUM_RESULTS,
            pause=DELAY
        ):
            if is_good_site(url):
                good_sites.append(url)
                print(f"Found good site: {url}")
            
            time.sleep(DELAY)  # Additional delay to be polite
            
    except Exception as e:
        print(f"Error during search: {str(e)}")
    
    return good_sites

# Only run this if the file is executed directly
if __name__ == "__main__":
    # Run the search and get the list
    mental_health_resources = find_mental_health_sites()
    
    # Print final results
    print("\nFound these potential mental health resources:")
    for i, url in enumerate(mental_health_resources, 1):
        print(f"{i}. {url}")