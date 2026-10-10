from typing import Annotated

from pydantic import BaseModel, StringConstraints, Field


class AskRequest(BaseModel):
    question: Annotated[str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=500
        )
    ] = Field(description="Customer question")


class AskResponse(BaseModel):
    answer: Annotated[str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
    )
    ] = Field(description="Service Response")