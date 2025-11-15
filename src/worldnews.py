import utils
import os
from article import Article

class WorldNewsClient:

    def __init__(self):
        pass

    def get_top_headlines(self, country="us", language="en", category="general", max_results=10):

        cache_file = f"data/{utils.today()}/worldnews-{country}-{language}-{category}.yaml"
        utils.ensure_basedir(cache_file)

        if os.path.exists(cache_file):
            data = utils.load_file(cache_file)
        else:
            import worldnewsapi

            configuration = worldnewsapi.Configuration(
               api_key = { "apiKey": "240e9483664f458983a947007c386b1a" }
            )
            with worldnewsapi.ApiClient(configuration) as api_client:
                # Create an instance of the API class
                api_instance = worldnewsapi.NewsApi(api_client)
                data = api_instance.top_news(country, language, var_date=None, headlines_only=False).to_dict()
        utils.save_file(cache_file, data)
            
        articles = data # [self.create_article(a) for a in data.get("articles", [])]
        return articles
    
    def create_article(self, data):
        data['source'] = data['source']['name']
        return Article(**data)        