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

    
    def __init__(self, page_info):
        self.id = str(page_info['pageid'])
        self.url = page_info['url']
        self.title = page_info['title']

    @classmethod
    def search(cls, full_name):
        formatted = full_name.replace(" ", "_")
        print(f"Buscando en API de Wikipedia: {full_name}")
        params = cls.API_PARAMS.copy()
        params.update({'titles': full_name})
        data = requests.get(cls.API_URL, params=params).json()
        if not data: return []
        pages = []
        for v in list(data['query']['pages'].values()):
            v['url'] = f'https://es.wikipedia.org/wiki/{formatted}'
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
                    ficha.update({f'WIKIPEDIA_{k.upper()}': v.split('|')[0]})
        return ficha 

    def get_info(self):
        print(f"Buscando en API de Wikipedia: {self.id}")
        response = {}
        params = self.API_PARAMS.copy()
        params.update({
            "pageids": self.id,
            'rvsection': '0',
            'rvprop': 'content', 
            'language': 'es',               
        })        
        data = requests.get(self.API_URL, params=params).json()
        if not data: return response

        # Obtener la información del infobox 
        pages = data['query']['pages']
        revision = pages[self.id]['revisions'][0]['*']
        infobox_dict = self.mw_to_dict(revision)
        wiki_ficha = self.process_ficha(infobox_dict)

        return wiki_ficha


