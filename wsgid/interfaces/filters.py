import plugnplay


class IPreRequestFilter(plugnplay.Interface):

    '''
     Receives the already parsed mongrel2 message object (wsgid.core.Message)
     and the WSGI environ
    '''
    def process(self, m2Message, environ):
        pass


class IPostRequestFilter(plugnplay.Interface):

    def process(self, m2message, status, body, heders):
        pass

    def exception(self, m2message, exception):
        pass
