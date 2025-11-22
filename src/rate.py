from article import Article
import ai
import json
from datetime import datetime

import utils

def rate_articles(articles: list[Article]):

    prompt = utils.load_file("prompts/relevance-scorer.md")
    for article in articles:
        prompt += f"## {article.title}\n"
        prompt += f"Source: {article.source}, {article.publishedAt.strftime('%c')}\n\n"
        prompt += f"{article.description}\n\n"
        prompt += f"{article.content}\n\n"

    ratings = json.loads(ai.exec(prompt, "rate articles"))
    for article, rating in zip(articles, ratings):
        article.score = rating['score']
        article.reasoning = rating['reasoning']

    # sort articles by score descending
    articles.sort(key=lambda a: a.score, reverse=True)
    
def is_important(article: Article) -> bool:
    return article.score >= 6 