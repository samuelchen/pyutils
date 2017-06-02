#!/usr/bin/env python
# coding: utf-8

"""
Django file related utilities
"""
from django.http import HttpResponse, StreamingHttpResponse


def download_file_response(fstream, filename='download.data', content_type='application/octet-stream'):
    """
    Download big file with yield (similar to "wsgiref.util.FileWrapper"). Fewer memory usage.
    :param request: the request
    :param fstream: file like object
    :param buf_size: buffer size for reading
    :return: HTTPStreamResponse instance
    """

    buf_size = 8192

    def _read_file_iter():
        while True:
            chunk = fstream.read(buf_size)
            if chunk:
                yield chunk
            else:
                raise StopIteration

    response = StreamingHttpResponse((c for c in _read_file_iter()), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    # response['Content-Length'] =
    return response