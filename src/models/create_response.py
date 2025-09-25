from typing import Union

from pydantic import BaseModel, StrictStr, StrictInt


class CreateResponse(BaseModel):
    id: Union[StrictInt, StrictStr]

    class Config:
        extra = "forbid"

