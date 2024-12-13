# python_scripts

This directory contains python scripts used in conjunction with mitmproxy
to monitor traffic and block and/or serve custom html pages to the built in web browser of the MG Marvel R we are pentesting.<br>
The scripts all essentially follow the same structure, with the difference being what happens after the redirect or block, and of course the content served in such cases.<br>

__redirect_poc.py__ is used to prove that the original request can be blocked and a custom page be served in response.<br>
__fake_login_with_redirect.py__ is what is used for the credential phishing. The original request is blocked, a custom login page is served in response. Information entered into the appropriate fields is sniffed using mitmproxy. After the log in button is pressed, an error page is displayed.
