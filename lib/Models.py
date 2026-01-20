import datetime
from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Any
from .Config import AUTHENTICATION_URI

class APIRequestModel(BaseModel):
    method: str = Field(default="GET")
    uri: HttpUrl = Field(default=AUTHENTICATION_URI)
    query_params: Dict[str, Any] = Field(default_factory=dict)
    headers: Dict[str, str] = Field(default_factory=dict)
    body: Dict[str, Any] = Field(default_factory=dict)
    class Config:
        # This helps if you log the model directly
        hide_input_in_errors = True

class MessageClass(BaseModel):
    id: str
    text: str
    timestamp: datetime.datetime