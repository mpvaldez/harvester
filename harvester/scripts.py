import pandas as pd

from harvester.sources.wikipedia import Wikipedia
from harvester.sources.wikidata import Wikidata

sources = ['wikipedia', 'wikidata']

def get_pages(entity:str):
    pages = {}
    wikipedia = Wikipedia.search(entity)
    if wikipedia:
        pages.update({'wikipedia': wikipedia[0]})
    wikidata = Wikidata.search(entity)
    if wikidata:
        pages.update({'wikidata': wikidata[0]})
    return pages

def collect(pages:dict):
    data = {}
    for k,v in pages.items():
        if k == 'wikipedia':
            wikipedia_page = Wikipedia(v)
            data.update(wikipedia_page.get_info())
        elif k == 'wikidata':
            wikidata_page = Wikidata(v)
            data.update(wikidata_page.get_info())            
    return data


def download(data:list):
    df = pd.DataFrame(data)
    return df.to_csv('output.csv')