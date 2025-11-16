from article import Article
import ai
import json
from datetime import datetime

import utils

def save_articles_as_markdown(articles: list[Article], filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# News Briefing\n\n")
        f.write(f"_Updated: {datetime.now().strftime("%c")}_\n\n")
        if articles:
            for article in articles:
                f.write(article_to_md(article))
        else:
            f.write("Nothing important happened in the last 12 hours.\n")

def article_to_md(article: Article) -> str:
    md = f"## {article.title}\n\n"
    md += f"[{article.source}]({article.url}), {article.publishedAt.strftime('%c')}\n\n"
    md += f"{article.description}\n\n"
    md += f"{article.content}\n"
    if article.score is not None:
        md += f"\n_Relevance score: [{article.score}] - {article.reasoning}_\n"
    return md

def rate_articles(articles: list[Article]):

    prompt = utils.load_file("prompts/relevance-scorer.md")
    for a in articles:
        prompt += "\n" + article_to_md(a)

    ratings = json.loads(ai.exec(prompt))
    for article, rating in zip(articles, ratings):
        article.score = rating['score']
        article.reasoning = rating['reasoning']

    # sort articles by score descending
    articles.sort(key=lambda a: a.score, reverse=True)
    
