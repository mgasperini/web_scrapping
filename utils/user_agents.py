import requests
from random import randint
import os



def get_user_agent_list():
    SCRAPE_OPS_API_KEY = os.getenv('SCRAPE_OPS_API_KEY')
    response = requests.get(
        f'http://headers.scrapeops.io/v1/user-agents?api_key={SCRAPE_OPS_API_KEY}'
    )
    json_response = response.json()
    return json_response.get('result', [])


def get_random_user_agent(user_agent_list=None):
    if user_agent_list is None:
        user_agent_list = get_user_agent_list()
    random_index = randint(0, len(user_agent_list) - 1)
    return user_agent_list[random_index]
