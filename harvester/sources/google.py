from selenium.webdriver.common.by import By

class Google:

    BASE_URL = "https://www.google.com/search?q="

    PROPERTIES = {
        'twitter.com': 'USER_TWITTER',
        'facebook.com': 'USER_FACEBOOK',
        'instagram.com': 'USER_INSTAGRAM',
        'youtube.com': 'USER_YOUTUBE',
    }

    def __init__(self, row, driver):
        self.full_name = str(row['full_name'])
        self.driver = driver
        
        
    def get_info(self):
        self.driver.get(self.BASE_URL+self.full_name+" politico")
        self.driver.implicitly_wait(10)
        response = {}
        for k, v in self.PROPERTIES.items():
            try:
                data = self.driver.find_element(By.XPATH, f'//a[contains(@href, "{k}")]')
                data = data.get_attribute('href').split('?')[0]
                response.update({v: data}) 
            except:
                print(f"Error al obtener información referenciada {v}")                
        return response

    # def __init__(self, full_name: str):

    #     try:
    #         self.results = Search(full_name, number_of_results=10).results
    #     except Exception as e:
    #         self.results = None
    #         print(f"{full_name} {e}")
        
    #     self.twitter_account = self.get_for("https://twitter.com")
    #     self.instagram_account = self.get_for("instagram.com")
    #     self.facebook_account = self.get_for("facebook.com")
    #     self.wikipedia_page = self.get_for("wikipedia.org")

    # def get_for(self, point):
    
    #     # Filtrar el elemento que contiene la referencia
    #     if not self.results:
    #         return
    #     any_results = next((result for result in self.results if point in result.url), None)
    #     if any_results:
    #         if any_results.url:
    #             return any_results.url.split('?')[0]

