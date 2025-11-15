from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    id: str
    title: str
    description: str
    content: str
    url: str
    image: str
    lang: str
    source: str
    publishedAt: datetime
    score: int
    reasoning: str