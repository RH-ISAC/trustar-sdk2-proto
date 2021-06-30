class TruStarResponse(object):

    def __init__(self, status_code, data, extra_args={}):
        self.status_code = status_code
        self.data = data
        self.extra_args = extra_args 
