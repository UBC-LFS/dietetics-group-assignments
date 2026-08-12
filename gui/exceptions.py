class MissingFieldError(Exception):
    def __init__(self, title, text):
        self.title = title
        self.text = text
        super().__init__(self.title)