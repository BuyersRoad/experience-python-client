
class ApiResponse:
    """Http response received.
    Attributes:
        text (string): The Raw body of the HTTP Response as a string
    """

    def __init__(self, http_response):
        """The Constructor
        Args:
            http_response (HttpResponse): The original, raw response from the api
        """

        self.status_code = http_response.status_code
        self.headers = http_response.headers
        self.text = http_response.text
        self.request = http_response.request

    def is_success(self):
        """ Returns true if status code is between 200-300
        """
        return 200 <= self.status_code < 300

    def is_error(self):
        """ Returns true if status code is between 400-600
        """
        return 400 <= self.status_code < 600

    def __repr__(self):
        return '<ApiResponse [%s]>' % (self.text)
