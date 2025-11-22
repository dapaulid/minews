from article import Article
import utils
import ai
import scraper

def summarize_article(article: Article) -> str:

    print(f'Retrieving full article: "{article.headline}"')
    content = scraper.get_full_article(article.url)

    prompt = utils.load_file('prompts/article-summarizer.md')
    prompt += f"# {article.title}\n\n{content}\n"

    summary = ai.exec(prompt, "summarize article")
    return summary
