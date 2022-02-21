import requests
from requests.auth import HTTPBasicAuth
import time

BASE_URL = 'https://e621.net/'
RATE_TIME = 1.5

class E621WrapperError(Exception):
    pass

class E621Wrapper:
    def __init__(self, username: str, api_key: str, user_agent: str = None, wait_for_rate_limit: bool = True) -> None:
        if not user_agent:
            self.user_agent = f'e621_scraper (by {username} on e621)'
        self.user_agent = str(user_agent)

        self._wait_for_rate_limit = wait_for_rate_limit
        self._last_requested = 0

        self._wrapper_session = requests.Session()
        self._wrapper_session.auth = HTTPBasicAuth(username, api_key)
        self._wrapper_session.headers.update({'User-Agent' : user_agent})

    def _wait(self) -> None:
        if self._wait_for_rate_limit:
            while True:
                if time.time() - self._last_requested > RATE_TIME:
                    return
    

    def get_posts(self, limit: int = 10, tags: list = [], page: str = None) -> dict:
        route = BASE_URL + 'posts.json'
        param_builder = {}
        
        if limit > 320:
            limit = 320
        param_builder['limit'] = limit

        tag_str = ' '.join(tags)
        param_builder['tags'] = tag_str

        if page:
            param_builder['page'] = page

        self._wait()
        self._last_requested = time.time()
        r = self._wrapper_session.get(route, params=param_builder)

        return r.json()['posts']
    
    def get_tags(self, limit: int = 75, category: int = None, page: str = None) -> dict:
        route = BASE_URL + 'tags.json'
        param_builder = {}
        
        if limit > 320:
            limit = 320
        param_builder['limit'] = limit

        if type(category) != type(int()):
            raise ValueError('Category must be type int()')

        if 0 <= category <= 8:
            param_builder['search[category]'] = category
        if page:
            param_builder['page'] = page

        self._wait()
        self._last_requested = time.time()
        r = self._wrapper_session.get(route, params=param_builder)

        return r.json()

        