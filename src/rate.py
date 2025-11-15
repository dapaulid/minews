from article import Article
import ai
import json

import utils

def save_articles_as_markdown(articles: list[Article], filename):
    with open(filename, "w", encoding="utf-8") as f:
        for article in articles:
            f.write(article_to_md(article))

def article_to_md(article: Article) -> str:
    md = f"# {article.title}\n\n"
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
    
