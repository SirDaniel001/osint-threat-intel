import requests
from stem import Signal
from stem.control import Controller
import time

# Tor proxy settings
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def get_ip():
    return requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10).json()['origin']

def renew_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Uses Tor cookie for authentication
        controller.signal(Signal.NEWNYM)

# Test identity rotation
if __name__ == "__main__":
    print("[INFO] Current IP:", get_ip())
    for i in range(3):
        print(f"[INFO] Rotating identity... ({i+1})")
        renew_identity()
        time.sleep(5)  # Wait for Tor to build new circuit
        print("[INFO] New IP:", get_ip())
