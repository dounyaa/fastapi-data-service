from fastapi import APIRouter

from app.schemas.echo import EchoRequest, EchoResponse

router = APIRouter(tags=["utils"])


@router.post("/echo", response_model=EchoResponse)
def echo(payload: EchoRequest) -> EchoResponse:
    result = " ".join([payload.text] * payload.count)
    return EchoResponse(result=result)
