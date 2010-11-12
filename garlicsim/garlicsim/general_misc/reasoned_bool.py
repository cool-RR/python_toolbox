
class ReasonedBool(object):
    def __init__(self, value, reason=None):
        self.value = bool(value)
        self.reason = reason
    def __repr__(self):
        return '<%s because %s>' % (self.value, repr(self.reason))
    def __bool__(self):
        return self.value
    __nonzero__ = __bool__