from pydantic import BaseModel, Field

class NewsEvent(BaseModel):
    title: str
    summary: str
    source: str
    published: str = ""
    link: str = ""