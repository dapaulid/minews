import requests
import utils
import os
from datetime import datetime, timezone, timedelta
from article import Article

class GNewsClient:
    BASE_URL = "https://gnews.io/api/v4/"

    def __init__(self):
        self.api_key = utils.getenv("GNEWS_API_KEY")

    def get_top_headlines(self, country="us", language="en", category="general", max_requests=5):

        cache_file = f"data/{utils.today()}/gnews-{country}-{language}-{category}.yaml"
        utils.ensure_basedir(cache_file)

        from_cache = os.path.exists(cache_file)
        if from_cache:
            fetched_articles = utils.load_file(cache_file)
        else:
            oldest = datetime.now(timezone.utc) - timedelta(days=1)
            params = {
                "apikey": self.api_key,
                "country": country,
                "lang": language,
                "category": category,
                "from": oldest.strftime('%Y-%m-%dT%H:%M:%SZ')
            }

            fetched_articles = []
            for i in range(max_requests):
                params["page"] = i + 1
                response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
                response.raise_for_status()
                data = response.json()
                page_articles = data["articles"]
                fetched_articles += page_articles
                if len(fetched_articles) < 10:
                    break
            utils.save_file(cache_file, fetched_articles)

        print(f"Fetched {len(fetched_articles)} articles from {'cache' if from_cache else 'API'}.")

        # parse articles
        articles = [self.create_article(a) for a in fetched_articles]
        return articles
    
    def create_article(self, data):
        data['source'] = data['source']['name']
        data['publishedAt'] = datetime.fromisoformat(data['publishedAt'])
        data['score'] = None
        data['reasoning'] = None
        return Article(**data)
