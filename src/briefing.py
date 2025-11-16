from article import Article
from datetime import datetime
import rate
import re

from babel.dates import format_datetime as babel_format_datetime

def format_md(articles: list[Article]) -> str:
    
    # split articles into important and unimportant
    important = [a for a in articles if rate.is_important(a)]
    unimportant = [a for a in articles if not rate.is_important(a)]

    md = f"_Aktualisiert: {format_datetime(datetime.now())}_\n\n"

    # output important articles first
    if important:
        md += format_articles(important)
    else:
        md += "Keine wichtigen Ereignisse in den letzten 12 Stunden.\n"
    # output unimportant articles in a collapsible section
    if unimportant:
        md += "\n<details>\n<summary>Unwichtige Ereignisse anzeigen</summary>\n\n"
        md += format_articles(unimportant)
        md += "\n</details>\n"

    return md

def format_articles(articles: list[Article]) -> str:
    md = ""
    for article in articles:
        md += f"## {article.title}\n\n"
        md += f"[{article.source}]({article.url}) • _{format_datetime(article.publishedAt)}_\n\n"
        md += f"{article.description}\n\n"
        md += format_content(article)
        md += f"\n\n_Relevance score: [{article.score}] - {article.reasoning}_\n"
    return md

def format_datetime(dt: datetime) -> str:
    # TODO localization
    return babel_format_datetime(dt, locale="de_CH", tzinfo="Europe/Zurich", format="EEEE, d. MMMM YYYY, hh:mm") + " Uhr"

def format_content(article: Article) -> str:
    return re.sub(r"\[\d+\s+chars\]", f"[weiterlesen]({article.url})", article.content)