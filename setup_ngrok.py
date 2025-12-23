import os
import sys
from pyngrok import ngrok, conf

def setup():
    token = os.environ.get("NGROK_AUTHTOKEN")
    if not token:
        print("Error: NGROK_AUTHTOKEN not set")
        sys.exit(1)
    
    print(f"Setting authtoken...")
    ngrok.set_auth_token(token)
    
    # Force binary install/check
    print("Checking ngrok binary...")
    path = conf.get_default().ngrok_path
    print(f"Ngrok binary path: {path}")
    
    # Try to connect briefly to verify
    # public_url = ngrok.connect(8000).public_url
    # print(f"Test tunnel created: {public_url}")
    # ngrok.disconnect(public_url)

if __name__ == "__main__":
    setup()
