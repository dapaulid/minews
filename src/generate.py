import gnews
import rate
import briefing
import utils
import argparse

# parse command line
parser = argparse.ArgumentParser(description="Generate news from filtered sources.")
parser.add_argument("-o", "--output-file", type=str, default="news.md",
    help="Path to the output markdown file.")
args = parser.parse_args()

# collect news articles
client = gnews.GNewsClient()
#client = worldnews.WorldNewsClient()
articles = client.get_top_headlines(country="ch", language="de")
# rate articles
rate.rate_articles(articles)
# save as markdown
utils.save_file(args.output_file, briefing.format_md(articles))
