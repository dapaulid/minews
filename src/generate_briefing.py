from briefing import Briefing
import utils
import argparse
import ai
import os
import translate

# parse command line
parser = argparse.ArgumentParser(description="Generate news from filtered sources.")
parser.add_argument("-o", "--output-dir", type=str, default="output/briefing",
    help="path to the output directory")
args = parser.parse_args()

# create briefing for Switzerland in German
briefing_de = Briefing(country="ch", language="de", category="general")
briefing_de_md = briefing_de.format_md()
# prepare German page with navigation
daily_md_de = "[DE] [[EN]](../en/daily.md)\n\n"
daily_md_de += "---\n\n"
daily_md_de += briefing_de_md
# save as markdown
utils.save_file(os.path.join(args.output_dir, "de/daily.md"), daily_md_de, create_dirs=True)

# create English translation
briefing_en_md = translate.translate_briefing(briefing_de_md, target_language="English")
# prepare English page with navigation
daily_md_en = "[[DE]](../de/daily.md) [EN]\n\n"
daily_md_en += "---\n\n"
daily_md_en += briefing_en_md
# save as markdown
utils.save_file(os.path.join(args.output_dir, "en/daily.md"), daily_md_en, create_dirs=True)

# print summary
ai.print_usage()
# done
print("\nCompleted successfully.")
