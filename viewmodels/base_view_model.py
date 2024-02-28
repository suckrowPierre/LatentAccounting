from typing import Optional
from fastapi import Request


class BaseViewModel:
    def __init__(self, request: Request):
        self.request = request
        self.error: Optional[str] = None

    def to_dict(self):
        return self.__dict__
