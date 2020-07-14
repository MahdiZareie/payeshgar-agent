
class ValidationError(ValueError):
    def __init__(self, detail: dict):
        self.detail = detail
