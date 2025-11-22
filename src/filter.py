from article import Article
import utils
import ai
import re

def filter_articles(articles: list[Article]) -> list[Article]:
        
        print("Article counts per source before filtering:")
        print_article_counts(articles)

        # de-duplicate articles
        articles = utils.deduplicate(articles, key_func=lambda a: a.title)
        articles = utils.deduplicate(articles, key_func=lambda a: a.url)
        print(f"After de-duplication by title/URL: {len(articles)} articles.")

        # filter out trash articles using AI
        prompt = utils.load_file('prompts/relevance-filter.md')
        for i, article in enumerate(articles):
            prompt += f"[{i}] {article.source} - {article.title}\n"
        response = ai.exec(prompt, "filter articles")

        keep_articles = []
        if response.strip() != "None.":
            for line in response.splitlines():
                m = re.match(r'\[(\d+)\] (.*) - (.*)', line)
                if m:
                    index = int(m.group(1))
                    source = m.group(2)
                    title = m.group(3)
                    assert source == articles[index].source
                    keep_articles.append(articles[index])
                else:
                    raise ValueError("Unrecognized line in filter response: %s" % line)
        
        print("Article counts per source after filtering:")
        print_article_counts(keep_articles)

        return keep_articles

def print_article_counts(articles: list[Article]):
    source_counts = {}
    for article in articles:
        source_counts[article.source] = source_counts.get(article.source, 0) + 1
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  [{count:>3}] {source}")
    print(f"  [{len(articles):>3}] TOTAL")
