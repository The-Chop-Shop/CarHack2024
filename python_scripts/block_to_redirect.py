from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is targeting the "/ap/oa" endpoint
    if "/ap/oa" in flow.request.pretty_url:
        # Check if the redirect_uri parameter matches the problematic URI
        if "redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia" in flow.request.pretty_url:
            # First, block the request with a 403 Forbidden response
            flow.response = http.Response.make(
                403,  # HTTP status code
                b"Blocked: redirect_uri not allowed.",  # Response body
                {"Content-Type": "text/plain"}  # Headers
            )
            # Log the blocking action
            print("Request blocked: ", flow.request.pretty_url)
            
            # Modify the request to redirect to a safer URI
            flow.request.url = flow.request.url.replace(
                "redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia",
                "redirect_uri=https%3A%2F%2Famazon.com"
            )
            # Log the redirection action
            print("Request redirected to: ", flow.request.url)

