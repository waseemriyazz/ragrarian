from pydantic import BaseModel

class Query(BaseModel):
    text: str

class Answer(BaseModel):
    text: str

class RephraseRequest(BaseModel):
    text: str
    format_option: str