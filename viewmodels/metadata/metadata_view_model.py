from fastapi import Request
from viewmodels.base_view_model import BaseViewModel


class PageMetadataViewModel(BaseViewModel):
    def __init__(self, request: Request, metadata: dict):
        super().__init__(request)
        self.title = metadata.get('title')
        self.description = metadata.get('description')
        self.keywords = metadata.get('keywords')
        self.author = metadata.get('author')
