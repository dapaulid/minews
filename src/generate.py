import gnews
import rate
import argparse

# parse command line
parser = argparse.ArgumentParser(description="Generate news from filtered sources.")
parser.add_argument("-o", "--output-file", type=str, default="news.md",
    help="Path to the output markdown file.")
args = parser.parse_args()

# do it
client = gnews.GNewsClient()
#client = worldnews.WorldNewsClient()
articles = client.get_top_headlines(country="ch", language="de")
rate.rate_articles(articles)
# discard low relevance articles
articles = [a for a in articles if a.score >= 6]
# save as markdown
rate.save_articles_as_markdown(articles, args.output_file)
