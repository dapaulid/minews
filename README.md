![Build](https://github.com/dapaulid/minews/actions/workflows/update-news.yml/badge.svg)

# [minews](https://dapaulid.github.io/minews) - Minimalist News Briefing

**minews** is an automated news aggregator that collects headlines from news sources, rates them for relevancy and generates an easy to read summary of the most important articles.

## Goals
- Provide an easy to read daily news briefing of the most relevant events.
- Remove the noise from everyday news - No clickbait, no sensationalism.
- Provide bullet-point summaries for articles, including links to [Wikipedia](https://www.wikipedia.org/) for background info.
- Focus on Switzerland, with briefings in German and English.

## How it Works
1. News update is started every day around 06:00 and 18:00 CET using a [GitHub Action](.github/workflows/update-news.yml).
2. Headlines from various news sources are collected from the last 24 hours.
3. The collected headlines are de-duplicated and filtered using AI.
4. The remaining headlines including a brief summary are scored for relevancy using AI.
5. For the most relevant headlines, the full article is fetched and summarized using AI.
6. The news briefing is generated in [Markdown](https://commonmark.org/) format and published using [Github Pages](https://docs.github.com/en/pages).

## Limitations
- News are delayed by 12 hours due to the use of a free-tier API.

## APIs Used

| API Name                              | Key Name             | Purpose                                  | 
|---------------------------------------|----------------------|------------------------------------------|
| [GNews.io](https://gnews.io/)         | `GNEWS_API_KEY`      | Get headlines from various news sources. |
| [OpenRouter](https://openrouter.ai/)  | `OPENROUTER_API_KEY` | Provide access to LLMs for news scoring, summarizing, translation, etc. |


## Similar Projects
- [News Minimalist](https://www.newsminimalist.com/)
