
from typing import Dict, Union
from pydantic import BaseModel

class BaseResponseSchema(BaseModel):
    #status: StatusType = StatusType.SUCCESS.value
    data: Union[Dict, None] = None
    message: str
    

    class Config:
        from_attributes = True