class ClientError(Exception):
    """
    Exception class is caught by websocket receive()
    and is sent back to the client.
    """
    def __init__(self, code):
        super(ClientError, self).__init__(code)
        self.code = code
