from selenium.webdriver.common.by import By

class Google:

    BASE_URL = "https://www.google.com/search?q="

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
        print(f"Buscando en Google: {self.search}")
        self.driver.get(self.BASE_URL+self.search)
        response = {}
        results = self.driver.find_elements(By.CSS_SELECTOR, '.g')
        for result in results:
            link = result.find_element(By.CSS_SELECTOR, 'a')
            url = link.get_attribute('href')
            for k, v in self.PROPERTIES.items():
                if url:
                    if k in url:
                        response.update({f'GOOGLE_{v}': link})
        return response
