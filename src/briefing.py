from article import Article
from datetime import datetime
import rate

def format_md(articles: list[Article]) -> str:
    
    # split articles into important and unimportant
    important = [a for a in articles if rate.is_important(a)]
    unimportant = [a for a in articles if not rate.is_important(a)]

    md = f"_Updated: {datetime.now().strftime("%c")}_\n\n"

    # output important articles first
    if important:
        md += format_articles(important)
    else:
        md += "Nothing important happened in the last 12 hours.\n"
    # output unimportant articles in a collapsible section
    if unimportant:
        md += "\n<details>\n<summary>Show unimportant news</summary>\n\n"
        md += format_articles(unimportant)
        md += "\n</details>\n"

    return md

def format_articles(articles: list[Article]) -> str:
    md = ""
    for article in articles:
        md += f"## {article.title}\n\n"
        md += f"[{article.source}]({article.url}), {article.publishedAt.strftime('%c')}\n\n"
        md += f"{article.description}\n\n"
        md += f"{article.content}\n"
        md += f"\n_Relevance score: [{article.score}] - {article.reasoning}_\n"
    return md
