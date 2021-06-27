class Success():
    def __init__(self, **kwargs):
        self.fromRequest = kwargs['from_request']
        self.statusCode = kwargs['status_code']
        self.data = kwargs['data']
        self.message = kwargs['message']
