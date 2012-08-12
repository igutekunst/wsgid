
Extending Wsgid
***************

.. _requestfilters:

Request Filters
---------------

.. versionadded:: 0.7.0

Request filters are extension points that Wsgid provides so you have an opportunity to inject custom code inside the flow of a Request. Currently you have two filters available: ``IPreRequestFilter`` and ``IPostRequestFilter``.

All Wsgid extension points are implemented through plugnplay (https://github.com/daltonmatos/plugnplay) project. To activate your custom filter, just drop your ``.py`` file inside your wsgidapp ``plugins/`` folder and restart your Wsgid process.


IPreRequestFilter
^^^^^^^^^^^^^^^^^

Invoked right before wsgid call to the running WSGI application. Since this call occurs after the mongrel2 message was parsed, this filter receives na copy of the raw message. Additionally it receives a copy of the WSGI environ that will be passes to the running application.

You can modify the WSGI environ freely, the modified version will be passed to the WSGI application. ::


    def IPreRequestFilter(plugnplay.Interface):

        def process(self, m2message, environ):
            pass


IPostRequestFilter
^^^^^^^^^^^^^^^^^^

Invoked after the WSGI application has returned its response. Receives also a copy of the raw mongrel2 message and additionally receives all values returned by the WSGI application. The HTTP status line, the generated response body and the headers (returned as a list of tuples, eg: ``[(<header-name>, <header-value>), ...])``.

This filter should always return a tuple containing the status line, the response body and the list of tuples (the headers). Even if you don't modify any value you must return them. This tuple will be expanded and will be passed to the next filter in the running chain.

If the WSGI application raises any Exception, the ``exception()`` method will be called receiving the raw mongrel2 message and a copy of the raised Exception. ::


    def IPostRequestFilter(plugnplay.Interface):

        def process(self, m2message, status, body, headers):
            pass

        def exception(self, m2message, e):
            pass
