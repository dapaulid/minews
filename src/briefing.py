from article import Article
from datetime import datetime, timezone
import gnews
import filter
import rate
import re
import summarize

from babel.dates import format_datetime as babel_format_datetime

class Briefing:

    important_articles: list[Article]
    unimportant_articles: list[Article]
    
    def __init__(self, country="us", language="en", category="general"):

        print(f"[ Creating briefing for country={country}, language={language}, category={category} ]")

        # collect news articles
        articles = gnews.get_top_headlines(country, language, category)
        # filter articles
        articles = filter.filter_articles(articles)
        # rate articles
        rate.rate_articles(articles)
        # split articles into important and unimportant
        self.important_articles = [a for a in articles if rate.is_important(a)]
        self.unimportant_articles = [a for a in articles if not rate.is_important(a)]
        # summarize important articles
        for article in self.important_articles:
            article.content = summarize.summarize_article(article)

        print(f"[ Briefing created: {len(self.important_articles)} important articles, {len(self.unimportant_articles)} unimportant articles ]")

    def format_md(self) -> str:
        # TODO localization
        md = f"_Aktualisiert: {self.format_datetime(datetime.now(timezone.utc))}_\n\n"

        # output important articles first
        if self.important_articles:
            md += self.format_articles(self.important_articles)
        else:
            md += "Keine wichtigen Ereignisse in den letzten 12 Stunden.\n"
        # output unimportant articles in a collapsible section
        if self.unimportant_articles:
            md += '\n<details><summary markdown="span">Unwichtige Ereignisse anzeigen</summary>\n\n'
            md += self.format_articles(self.unimportant_articles)
            md += "\n</details>\n"
        return md

    def format_articles(self, articles: list[Article]) -> str:
        md = ""
        for article in articles:
            md += f"## {article.title}\n\n"
            md += f"[{article.source}]({article.url}) • _{self.format_datetime(article.publishedAt)}_\n\n"
            md += f"{article.description}\n\n"
            md += self.format_content(article)
            md += f"\n\n>Relevance score: [{article.score}] - {article.reasoning}\n\n"
        return md

    def format_datetime(self, dt: datetime) -> str:
        # TODO localization
        return babel_format_datetime(dt, locale="de_CH", tzinfo="Europe/Zurich", format="EEEE, d. MMMM YYYY, HH:mm") + " Uhr"

    def format_content(self, article: Article) -> str:
        # TODO localization
        return re.sub(r"\[\d+\s+chars\]", f"[weiterlesen]({article.url})", article.content)
