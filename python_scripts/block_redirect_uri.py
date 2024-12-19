from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is targeting the "/ap/oa" endpoint
    if "/ap/oa" in flow.request.pretty_url:
        # Check if the redirect_uri parameter matches the problematic URI
        if "redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia" in flow.request.pretty_url:
            # Block the request by sending a 403 Forbidden response
            flow.response = http.Response.make(
                403,  # HTTP status code
                b"Blocked: redirect_uri not allowed.",  # Response body
                {"Content-Type": "text/plain"}  # Headers
            )

