
import requests

# Creo la clase para analizar cosas desde wikipedia
class Wikidata:
    """
        Wikidata via API y los elementos referenciados via scrapping
    """

    API_URL = 'https://www.wikidata.org/w/api.php'
    API_PARAMS = {
        'language': 'es',
        'format': 'json'
    }    


    PROPERTIES = {
        "P735": 'NOMBRE',
        "P734": 'APELLIDO',
        "P1449": 'APODO',
        "P19": 'LUGAR_NACIMIENTO',
        "P569": 'FECHA_NACIMIENTO',
        "P21": 'GENERO',
        "P2002": 'USER_TWITTER',
        "P2013": 'USER_FACEBOOK',
        "P2003": 'USER_INSTAGRAM',
        "P1971": 'NUMERO_HIJXS',
        "P69": 'EDUCADO_EN',
        'P18': 'IMAGEN',
        "P39": 'PUESTO_ANTERIOR', # Hay que buscar la forma de captar mas de 1
        "P106": 'OCUPACION' # Hay que buscar la forma de captar mas de 1
    }

    def __init__(self, page_info):
        self.id = page_info.split('/')[-1]


    @classmethod
    def search(cls, entity):
        print(f"Buscando en API de Wikidata: {entity}")
        params = cls.API_PARAMS
        params.update({
            'action': 'wbsearchentities',
            'search': entity
        })
        data = requests.get(cls.API_URL, params=params).json()
        if not data['search']:return []

        pages = []
        for d in data['search']:
            d['url'] = f"https:{d['url']}"
            pages.append(d)
        return pages


    def get_referenced_info(self, referenced_id): 
        params = self.API_PARAMS
        params.update({
            "action": "wbgetentities",
            "ids": referenced_id,
            "props": "labels"
        })
        response = requests.get(self.API_URL, params=params).json()
        if not response or not "entities" in response.keys(): return ''
        return response['entities'][referenced_id]['labels']['es']['value']

    def get_info(self): 
        print(f"Extrayendo desde API de Wikidata: {self.id}")
        data = {}
        params = self.API_PARAMS
        params.update({
            "action": "wbgetentities",
            "ids": self.id,
            "props": "claims"
        })        
        response = requests.get(self.API_URL, params=params).json()
        if not response or not "entities" in response.keys(): return data
        
        claims = response["entities"][self.id]["claims"]
        for k, v in self.PROPERTIES.items():
            if k in claims:
                for i in range(len(claims[k])):
                    q = i-1
                    prefix_value = f'WIKIDATA_{v}'
                    if q > 0:
                        prefix_value+=f'{q}'
                    data_type = claims[k][q]["mainsnak"]["datavalue"]['type']
                    data_value = claims[k][q]["mainsnak"]["datavalue"]["value"]
                    if data_type == "wikibase-entityid":
                        try:    
                            referenced_data = self.get_referenced_info(data_value['id'])
                            data.update({prefix_value: referenced_data})
                        except:
                            print(f"Error al obtener información referenciada {v}")
                    elif data_type == "string":
                        data.update({prefix_value: data_value})
                    elif data_type == "time":
                        data.update({prefix_value: data_value['time'].replace("+", "").split("T")[0]})

        return data


