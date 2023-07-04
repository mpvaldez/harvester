import re
import requests
import mwparserfromhell

class Wikipedia:

    """
        Wikipedia via API
    """

    API_URL = 'https://es.wikipedia.org/w/api.php'
    API_PARAMS = {
        'format': 'json',
        'action': 'query',
        'prop': 'revisions',
    }    

    REMOVE_KEYS = [
        r'.*PIE.*', 
        r'.*ESCUDO.*', 
        r'.*PRESIDEN.*',
        r'.*SUBTÍTULO.*',
        r'.*DATA.*',
        r'.*SUCESOR.*',
        r'.*PREDECESOR.*',
        r'.*EXCÓNYUGE.*',
        r'.*TAMAÑO.*',
        r'.*DESCRIPCIÓN.*',
        r'.*NOTAS.*',
        r'.*FIRMA.*',
        r'.*TRATAMIENTO.*',
        r'.*JUNTOA.*',
    ]

    
    def __init__(self, entity):
        self.entity = entity

    @classmethod
    def search(cls, entity):
        print(f"Buscando en API de Wikipedia: {entity}")
        params = cls.API_PARAMS.copy()
        params.update({'titles': entity})
        data = requests.get(cls.API_URL, params=params).json()
        if not data: return []
        pages = []
        for v in list(data['query']['pages'].values()):
            v['url'] = f'https://es.wikipedia.org/wiki/{entity}'
            pages.append(v)
        return pages

    @classmethod
    def mw_to_dict(cls, wiki_text):
        # Parsear el contenido del infobox utilizando mwparserfromhell
        wikicode = mwparserfromhell.parse(wiki_text)

        # Convertir el contenido del infobox a un objeto JSON
        infobox_dict = {}
        for template in wikicode.filter_templates():
            template_dict = {}
            for param in template.params:
                param_name = param.name.strip()
                param_value = param.value.strip_code().strip()
                template_dict[param_name] = param_value
            infobox_dict[template.name.strip()] = template_dict 

        return infobox_dict


    def process_ficha(self, infobox_dict):
        ficha = {}
        any_ficha = [k for k in infobox_dict.keys() if 'ficha de' in k.lower()]
        if any_ficha:
            data = infobox_dict[any_ficha[0]]
            for k, v in data.items():
                if k in data:
                    ficha.update({f'WIKIPEDIA_{k.upper().replace(" ", "_")}': v.split('|')[0]})
        return ficha 
    

    def clean_ficha(self, wiki_ficha):
        for k in list(wiki_ficha.keys()):
            for regex in self.REMOVE_KEYS:
                if re.match(regex, k) and k in wiki_ficha.keys():
                    del wiki_ficha[k]
        for i in range(10):
            key = f'WIKIPEDIA_{i}'
            if key in list(wiki_ficha.keys()):
                del wiki_ficha[key]
        return wiki_ficha    

    def get_info(self):
        print(f"Extrayendo desde API de Wikipedia: {self.entity}")
        response = {}
        params = self.API_PARAMS.copy()
        params.update({
            'titles': self.entity,
            'rvsection': '0',
            'rvprop': 'content', 
        })        
        data = requests.get(self.API_URL, params=params).json()
        if not data or not 'query' in data.keys(): return response

        # Obtener la información del infobox 
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        
        if not 'revisions' in pages[page_id]: return response
        
        revision = pages[page_id]['revisions'][0]['*']
        infobox_dict = self.mw_to_dict(revision)
        wiki_ficha = self.process_ficha(infobox_dict)
        clean_ficha = self.clean_ficha(wiki_ficha)

        return clean_ficha


