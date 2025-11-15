import gnews
import worldnews
import rate
import utils

def main():
    client = gnews.GNewsClient()
    #client = worldnews.WorldNewsClient()
    articles = client.get_top_headlines(country="ch", language="de")
    rate.rate_articles(articles)

    newsletter_file = f"data/{utils.today()}/newsletter.md"
    utils.ensure_basedir(newsletter_file)    
    rate.save_articles_as_markdown(articles, newsletter_file)

if __name__ == "__main__":
    main()
