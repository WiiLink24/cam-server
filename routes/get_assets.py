from flask import send_file, request

def get_assets(_request):
  if request.headers.get("Version") == "1.0.0":
    return ""

  resp = send_file("00000002.app")
  resp.headers.set("Version", "1.0.0")
  return resp
