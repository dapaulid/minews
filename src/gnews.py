import requests
import utils
import os
from datetime import datetime
from article import Article

class GNewsClient:
    BASE_URL = "https://gnews.io/api/v4/"

    def __init__(self):
        self.api_key = utils.getenv("GNEWS_API_KEY")

    def get_top_headlines(self, country="us", language="en", category="general", max_results=10):

        cache_file = f"data/{utils.today()}/gnews-{country}-{language}-{category}.yaml"
        utils.ensure_basedir(cache_file)

        if os.path.exists(cache_file):
            data = utils.load_file(cache_file)
        else:
            params = {
                "apikey": self.api_key,
                "country": country,
                "lang": language,
                "category": category,
                "max": max_results
            }

            response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
            response.raise_for_status()
            data = response.json()
            utils.save_file(cache_file, data)
            
        articles = [self.create_article(a) for a in data.get("articles", [])]
        return articles
    
    def create_article(self, data):
        data['source'] = data['source']['name']
        data['publishedAt'] = datetime.fromisoformat(data['publishedAt'])
        data['score'] = None
        data['reasoning'] = None
        return Article(**data)
