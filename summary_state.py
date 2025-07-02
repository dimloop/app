import operator
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage

class State(TypedDict):
    article: dict
    article_text: str
    summary: str
    summary_7: str
    summary_1: str
    explanations: str
    questions: str
    answers: str
    feedback: str
    evaluation_complete: bool
    iteration_count: int
    output_path: str
