from urllib.parse import urlparse

from selenium.webdriver.common.by import By

class Google:

    BASE_URL = "https://www.google.com/search?q="

    PROPERTIES = {
        'twitter.com': 'USER_TWITTER',
        'facebook.com': 'USER_FACEBOOK',
        'instagram.com': 'USER_INSTAGRAM',
        'youtube.com': 'USER_YOUTUBE',
    }

    def __init__(self, search, driver):
        self.search = search
        self.driver = driver
        
        
    def get_info(self):
        print(f"Buscando en Google: {self.search}")
        self.driver.get(self.BASE_URL+self.search)
        self.driver.implicitly_wait(5)
        response = {}
        for k, v in self.PROPERTIES.items():
            try:
                elements = self.driver.find_elements(By.TAG_NAME, "a")
                links = list(set([el.get_attribute('href').split("?")[0] for el in elements if el.get_attribute('href')]))
                for link in links:
                    if k in link:
                        response.update({f'GOOGLE_{v}': link})
                        break
            except:
                print(f"Error al obtener información referenciada {v}")                
        return response
