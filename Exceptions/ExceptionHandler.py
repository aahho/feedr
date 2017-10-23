from flask import jsonify

class FeedrException(Exception):

    def __init__(self, message, status_code=500, payload=None, hint=None):
        Exception.__init__(self)
        self.message = message
        self.hint = hint
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['data'] = []
        rv['code'] = self.status_code
        rv['notification'] = {
            'seCode' : 'SE_'+str(self.status_code),
            'message' : self.message,
            'hint' : self.hint,
            'type' : 'error'
        }
        rv['version'] = 1
        return rv