class AgentAPIError(Exception):
    """Exception raised when agent API call fails"""
    def __init__(self, message: str, status_code: int = None, details: str = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

class NetworkError(Exception):
    """Exception raised when network request fails"""
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class ValidationError(Exception):
    """Exception raised when request validation fails"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

