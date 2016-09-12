class MessageException(BaseException):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.__class__.__name__ + ':' + self.message
