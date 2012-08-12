
from time import time
from wsgid.interfaces.filters import IPostRequestFilter, IPreRequestFilter
from wsgid.core import Plugin


r = {}


# Example of two filters that works togheter.
# The PreRequestFilter uses the wsgid.core.Message to store the
# Start time fo the request.
#
# After the WSGI app is called, the PostRequestFilter calculates
# the amount of time the request took to run completely.
#
# Note that this time can potentially not be accuarte. If you have many
# PostRequestFilters and this filters happens to be the last one in the
# execution chain, the final calculated time will be distorted.


class CalcTimePreReqFilter(Plugin):

    implements = [IPreRequestFilter, ]

    def process(self, message, environ):
        r[message.client_id] = time()


class CalcTimePostReqFilter(Plugin):

    implements = [IPostRequestFilter, ]

    def process(self, message, status, headers, body):
        elapsed = time() - r[message.client_id]
        del r[message.client_id]
        return (status, headers + [('X-Time', "{0} ms".format(str(elapsed)))], body)

    def exception(self, message, e):
        pass
