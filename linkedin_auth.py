#!/usr/bin/env python3
"""LinkedIn OAuth 2.0 helper — genereert een access token met de juiste scopes."""

import http.server
import urllib.parse
import requests
import sys

CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
REDIRECT_URI = "http://localhost:8585/callback"
SCOPES = "openid profile w_member_social"

auth_code = None

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        auth_code = params.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Gelukt! Je kunt dit venster sluiten.</h1>")

    def log_message(self, format, *args):
        pass  # stille server

def main():
    # Stap 1: Toon autorisatie-URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
        f"&scope={urllib.parse.quote(SCOPES)}"
        f"&state=blog_automator"
    )

    print("\n=== LinkedIn OAuth ===")
    print(f"\n1. Open deze URL in je browser:\n")
    print(auth_url)
    print(f"\n2. Log in en klik 'Allow'")
    print(f"3. Je wordt teruggestuurd naar localhost — het script vangt dat op.\n")
    print("Wachten op callback...")

    # Stap 2: Start lokale server om callback op te vangen
    server = http.server.HTTPServer(("localhost", 8585), CallbackHandler)
    server.handle_request()

    if not auth_code:
        print("❌ Geen autorisatiecode ontvangen.")
        sys.exit(1)

    print(f"✅ Autorisatiecode ontvangen!")

    # Stap 3: Wissel code in voor access token
    print("🔄 Token ophalen...")
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    if response.status_code != 200:
        print(f"❌ Fout: {response.status_code} - {response.text}")
        sys.exit(1)

    data = response.json()
    token = data["access_token"]
    expires = data.get("expires_in", "?")
    scope = data.get("scope", "?")

    print(f"\n{'='*60}")
    print(f"✅ ACCESS TOKEN VERKREGEN!")
    print(f"   Scopes:  {scope}")
    print(f"   Geldig:  {int(expires)//86400} dagen")
    print(f"{'='*60}")
    print(f"\nToken:\n{token}\n")

    # Stap 4: Schrijf naar .env
    env_path = "blog-automator/.env" if not __file__.startswith("/") else "/Users/stefanbalkenende/blog-automator/.env"
    with open("/Users/stefanbalkenende/blog-automator/.env", "r") as f:
        env = f.read()

    import re
    env = re.sub(r"LINKEDIN_ACCESS_TOKEN=.*", f"LINKEDIN_ACCESS_TOKEN={token}", env)

    with open("/Users/stefanbalkenende/blog-automator/.env", "w") as f:
        f.write(env)

    print("✅ Token opgeslagen in .env!")

if __name__ == "__main__":
    main()
