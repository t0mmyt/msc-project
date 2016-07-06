class ObservationError(Exception):
    """
    Exception to contain all errors relating to loading the observations
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
