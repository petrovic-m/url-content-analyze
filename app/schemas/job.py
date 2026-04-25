from pydantic import BaseModel, HttpUrl

class JobCreateRequest(BaseModel):
    url: HttpUrl