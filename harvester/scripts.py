import pandas as pd
from selenium import webdriver

from harvester.sources.wikipedia import Wikipedia
from harvester.sources.wikidata import Wikidata
from harvester.sources.google import Google
from harvester.sources.duckduckgo import DuckDuckGo

def prepare_entities(entities:list) -> pd.DataFrame:
    return pd.DataFrame({'entity': entities})

def get_pages(entities:pd.DataFrame) -> pd.DataFrame:
    """
        Get pages links from wikipedia and wikidata
        ----------
        params
            entities : pandas.DataFrame
        -------
        return pandas.DataFrame
    """

    pages = {
        'entity': [],
        'WIKIPEDIA_URL': [],
        'WIKIDATA_URL': []
    }
    for _, row in entities.iterrows():
        formatted = row['entity'].replace(" ", "_")
        pages['entity'].append(row['entity'])
        
        wikipedia = Wikipedia.search(row['entity'])
        if wikipedia:
            pages['WIKIPEDIA_URL'].append(wikipedia[0]['url'] if 'url' in wikipedia[0].keys() else '')
        else:
            pages['WIKIPEDIA_URL'].append('')
        
        wikidata = Wikidata.search(row['entity'])
        if wikidata:
            pages['WIKIDATA_URL'].append(wikidata[0]['url'] if 'url' in wikidata[0].keys() else '')
        else:
            pages['WIKIDATA_URL'].append('')

    return pd.DataFrame(pages)

def collect_from_wikipedia(pages_list:pd.DataFrame) -> pd.DataFrame:
    """
        Collect information from pages
        ----------
        params
            pages_list : pandas.DataFrame
            keyword : str
        -------
        return pandas.DataFrame              
    """

    datos = {}
    for _, row in pages_list.iterrows():
        formatted = row['entity'].replace(" ", "_")
        datos[formatted] = {'entity': row['entity']}

        # From wikipedia
        if not pd.isna(row['WIKIPEDIA_URL']):
            wikipedia_page = Wikipedia(formatted).get_info()
            datos[formatted].update(wikipedia_page)    

    df = pd.DataFrame(datos.values())
    return df

def collect_from_wikidata(pages_list:pd.DataFrame) -> pd.DataFrame:
    """
        Collect information from pages
        ----------
        params
            pages_list : pandas.DataFrame
            keyword : str
        -------
        return pandas.DataFrame              
    """

    datos = {}
    for _, row in pages_list.iterrows():
        formatted = row['entity'].replace(" ", "_")
        datos[formatted] = {'entity': row['entity']}

        # # From wikidata
        if not pd.isna(row['WIKIDATA_URL']):
            wikidata_page = Wikidata(row['WIKIDATA_URL']).get_info()
            datos[formatted].update(wikidata_page)

    df = pd.DataFrame(datos.values())
    return df


def collect_from_google(entities:pd.DataFrame, keyword:str="") -> pd.DataFrame:
    """
        Collect information from pages
        ----------
        params
            pages_list : pandas.DataFrame
            keyword : str
        -------
        return pandas.DataFrame              
    """
    driver = webdriver.Firefox()
    datos = {}
    for _, row in entities.iterrows():
        formatted = row['entity'].replace(" ", "_")
        datos[formatted] = {'entity': row['entity']}

        # From google
        search = f"{row['entity']} {keyword}"
        google_info = Google(search, driver).get_info()
        datos[formatted].update(google_info)            
    driver.quit()
    df = pd.DataFrame(datos.values())
    return df


def collect_from_duckduckgo(entities:pd.DataFrame, keyword:str="") -> pd.DataFrame:
    """
        Collect information from duckduckgo
        ----------
        params
            pages_list : pandas.DataFrame
            keyword : str
        -------
        return pandas.DataFrame              
    """
    driver = webdriver.Firefox()
    datos = {}
    for _, row in entities.iterrows():
        formatted = row['entity'].replace(" ", "_")
        datos[formatted] = {'entity': row['entity']}

        search = f"{row['entity']} {keyword}"
        duckduckgo_info = DuckDuckGo(search, driver).get_info()
        datos[formatted].update(duckduckgo_info)            
    driver.quit()
    df = pd.DataFrame(datos.values())
    return df






def download(data:list, name:str="output"):
    df = pd.DataFrame(data)
    df.to_csv(f'{name}.csv', index=False)