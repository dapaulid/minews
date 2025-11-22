import gnews
import rate
import briefing
import utils
import argparse
import filter
import ai

# parse command line
parser = argparse.ArgumentParser(description="Generate news from filtered sources.")
parser.add_argument("-o", "--output-file", type=str, default="news.md",
    help="Path to the output markdown file.")
args = parser.parse_args()

# collect news articles
client = gnews.GNewsClient()
articles = client.get_top_headlines(country="ch", language="de")
# filter articles
articles = filter.filter_articles(articles)
# rate articles
rate.rate_articles(articles)
# save as markdown
utils.save_file(args.output_file, briefing.format_md(articles))
# print summary
ai.print_usage()
# done
print("\nCompleted successfully.")
