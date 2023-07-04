import json
import requests

class DuckDuckGo:

    URL = 'https://api.duckduckgo.com/?q={}&format=json'
    BASES = {
        'twitter_profile':'https://twitter.com/',
        'facebook_profile':'https://facebook.com/',
        'instagram_account':'https://instagram.com/',
    }


    def __init__(self, entity: str):
        result = requests.get(self.URL.format(entity))
        self.result = json.loads(result.content.decode('utf-8'))
        self.twitter_account = self.from_infobox('twitter_profile')
        self.facebook_account = self.from_infobox('facebook_profile')
        self.instagram_account = self.from_infobox('instagram_account')
        self.wikipedia_page = self.result['AbstractURL'] or None


    def from_infobox(self, point):
        if not self.result["Infobox"]:
            return
        value = next((item["value"] for item in self.result["Infobox"]["content"] if item["data_type"] == point), None)
        if not value:
            return 
        return self.BASES[point]+value



