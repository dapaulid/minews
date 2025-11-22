import requests
import utils
import os
import time
from timeit import default_timer as timer
from datetime import datetime, timezone, timedelta
from article import Article

def get_top_headlines(country="us", language="en", category="general", max_requests=10) -> list[Article]:

    # The free tier of gnews.io API includes the following:
    # - 100 requests per day
    # - Up to 10 articles returned per request
    # - 10 requests/minute
    # - 12-hour delay
    # - 30 days historical data
    # - one request per second / 60 requests per minute?

    print(f"Fetching top headlines from GNews...")

    cache_file = f"data/{utils.today()}/gnews-{country}-{language}-{category}.yaml"
    utils.ensure_basedir(cache_file)

    start_time = time.time()
    from_cache = os.path.exists(cache_file)
    if from_cache:
        fetched_articles = utils.load_file(cache_file)
    else:
        oldest = datetime.now(timezone.utc) - timedelta(days=1)
        params = {
            "apikey": utils.getenv("GNEWS_API_KEY"),
            "country": country,
            "lang": language,
            "category": category,
            "from": oldest.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        fetched_articles = []
        for i in range(max_requests):
            params["page"] = i + 1
            if i > 0:
                time.sleep(1.0)  # to respect rate limits
            print(f"  fetching page #{i+1}...")
            response = requests.get(f"https://gnews.io/api/v4/top-headlines", params=params)
            response.raise_for_status()
            data = response.json()
            page_articles = data["articles"]
            fetched_articles += page_articles
            if len(page_articles) < 10:
                break
        utils.save_file(cache_file, fetched_articles)

    duration = time.time() - start_time
    print(f"  done, fetched {len(fetched_articles)} articles from {'cache' if from_cache else 'API'}, took {duration:.3f} seconds.")

    # parse articles
    articles = [parse_article(a) for a in fetched_articles]
    return articles
    
def parse_article(data):
    data['source'] = data['source']['name']
    data['publishedAt'] = datetime.fromisoformat(data['publishedAt'])
    data['score'] = None
    data['reasoning'] = None
    return Article(**data)
