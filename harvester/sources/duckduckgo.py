from selenium.webdriver.common.by import By

class DuckDuckGo:

    BASE_URL = 'https://duckduckgo.com/?q='

    PROPERTIES = {
        'twitter.com': 'USER_TWITTER',
        'facebook.com': 'USER_FACEBOOK',
        'instagram.com': 'USER_INSTAGRAM',
        'linkedin.com': 'USER_LINKEDIN',
        'wikipedia.org': 'PAGE_WIKIPEDIA',
    }


    def __init__(self, search, driver):
        self.search = search
        self.driver = driver
        
        
    def get_info(self):
        print(f"Buscando en DuckDuckGo: {self.search}")
        self.driver.get(self.BASE_URL+self.search)
        response = {}
        results = self.driver.find_elements(By.CSS_SELECTOR, '.react-results--main')
        for result in results:
            articles = result.find_elements(By.TAG_NAME, 'article')
            for article in articles:
                links = article.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    url = link.get_attribute('href')
                    if not 'duckduckgo.com' in url:
                        for k, v in self.PROPERTIES.items():
                            if k in url:
                                key = f'DUCKDUCKGO_{v}'
                                if not key in response.keys():
                                    response.update({key: url})
        return response
