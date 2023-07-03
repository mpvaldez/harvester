# from selenium import webdriver
# from selenium.webdriver.common.by import By


# # Creo la clase para analizar cosas desde twitter
# class Twitter:
#     """
#         Con selenium dado que es una web que carga la data dinamicamente
#             Selenium navega y captura elementos
#     """    

#     seguidores = ""

#     def __init__(self, url, webdriver):
        
#         if url:
#             print(f"Scrappeanding {url}")
#             self.driver = webdriver
#             # Abrir la página de Twitter
#             self.driver.get(url)

#             # Esperar a que la página cargue completamente
#             self.driver.implicitly_wait(10)

#             self.process_account()


#     def process_account(self):
#         self.seguidores = self.driver.find_element(By.XPATH, '//a[contains(@href, "/followers")]').text


