import newspaper

def get_full_article(url: str) -> str:
    a = newspaper.Article(url)
    a.download()
    a.parse()
    return a.text
