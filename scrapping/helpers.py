import requests
from utils.user_agents import get_random_user_agent
import os


def get_request(url):
    SCRAPE_OPS_API_KEY = os.getenv('SCRAPE_OPS_API_KEY')
    URL_PROXY = 'https://proxy.scrapeops.io/v1/'
    PARAMS_PROXY = {
        'api_key': SCRAPE_OPS_API_KEY,
        'url': url,
    }
    headers = {'User-Agent': get_random_user_agent()}
    try:
        response = requests.get(
            URL_PROXY,
            params=PARAMS_PROXY,
            headers=headers,
            timeout=120,
        )
        print(response.status_code)
        return response.content
    except:
        return None


def get_page_url_status_code(url, driver):
    for request in driver.requests:
        if request.response:
            print(request.url, request.response.status_code,
                  request.response.headers['Content-Type'])
        if request.url == url:
            return request.response.status_code
    return 500


def interceptor(request):
    if request.path.endswith(
        ('.png', '.jpg', '.gif', '.css')) or 'fonts.' in request.path:
        request.abort()
