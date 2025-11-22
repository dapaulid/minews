from briefing import Briefing
import utils
import argparse
import ai

# parse command line
parser = argparse.ArgumentParser(description="Generate news from filtered sources.")
parser.add_argument("-o", "--output-file", type=str, default="news.md",
    help="path to the output markdown file")
parser.add_argument("--country", type=str, default="ch",
    help="country code for news localization (default: ch)")
parser.add_argument("--language", type=str, default="de",
    help="language code for news localization (default: de)")
parser.add_argument("--category", type=str, default="general",
    help="news category (default: general)")
args = parser.parse_args()

# create briefing
briefing = Briefing(country=args.country, language=args.language, category=args.category)
# save as markdown
utils.save_file(args.output_file, briefing.format_md())

# print summary
ai.print_usage()
# done
print("\nCompleted successfully.")
