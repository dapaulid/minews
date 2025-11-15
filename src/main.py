import gnews
import rate

def main():
    client = gnews.GNewsClient()
    #client = worldnews.WorldNewsClient()
    articles = client.get_top_headlines(country="ch", language="de")
    rate.rate_articles(articles)
    rate.save_articles_as_markdown(articles, "news.md")

if __name__ == "__main__":
    main()
