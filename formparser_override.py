from werkzeug import exceptions
from werkzeug.formparser import parse_multipart_headers

to_find = 'form-data; name="jpegData"'
to_replace = 'form-data; name="jpegData"; filename="jpegData"'


def parse_multipart_headers_fix(iterable):
    # Nintendo, in their ever infinite wisdom,
    # separate the sent file's name in a field named "imageFileName".
    # Actual JPEG data, however, is sent in a field named "jpegData".
    #
    # Werkzeug interprets "jpegData" as being a form value (instead of a file)
    # due to this lack of parameter and attempts to encode the raw binary value
    # sent as an UTF-8 string, which as of writing is its default charset.
    #
    # (As a bit of trivia, RFC2183 - https://tools.ietf.org/html/rfc2183 -
    # does not appear to require this. So we must hack around this...)

    headers = parse_multipart_headers(iterable)
    if not headers:
        # No headers is silly and will break us later on.
        return exceptions.BadRequest()

    # Look for our faulty "jpegData" data.
    for key, value in headers:
        if value == to_find:
            # Make "jpegData" have a filename.
            headers[key] = to_replace

    return headers
