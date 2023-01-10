from werkzeug.datastructures import Headers
from werkzeug.exceptions import BadRequest
from werkzeug.sansio.multipart import MultipartDecoder

to_find = 'form-data; name="jpegData"'
to_replace = 'form-data; name="jpegData"; filename="jpegData"'

# Hold our old function in order to call it within our patch.
_old_parse_headers = MultipartDecoder._parse_headers


def _parse_headers_fix(self, data: bytes) -> Headers:
    """A hack to parse files properly in a multipart form.

        Nintendo, in their ever infinite wisdom,
    separate the sent file's name in a field named "imageFileName".
    Actual JPEG data, however, is sent in a field named "jpegData".

    Werkzeug interprets "jpegData" as being a form value (instead of a file)
    due to this lack of parameter and attempts to encode the raw binary value
    sent as an UTF-8 string, which as of writing is its default charset.

    (As a bit of trivia, RFC2183 - https://tools.ietf.org/html/rfc2183 -
    does not appear to require this. So we must hack around this...)"""

    # Call the original function.
    headers = _old_parse_headers(self, data)
    if not headers:
        # Providing no headers is invalid and will break us later on.
        raise BadRequest

    # Determine if we have Content-Disposition.
    value = headers.get("Content-Disposition", type=str)
    if not value:
        # This isn't the request we need to patch.
        return headers

    # Determine whether this has our faulty jpegData header.
    if value == to_find:
        # We simply replace with a header containing a valid filename.
        headers.set("Content-Disposition", to_replace)

    return headers


# Replace.
MultipartDecoder._parse_headers = _parse_headers_fix
