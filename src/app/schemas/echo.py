from pydantic import BaseModel, Field


class EchoRequest(BaseModel):
    text: str = Field(
        min_length=1,
    )
    count: int = Field(
        ge=1,
        le=10,
    )


class EchoResponse(BaseModel):
    result: str
