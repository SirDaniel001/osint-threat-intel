import requests

# Check IP without Tor
normal_ip = requests.get("https://httpbin.org/ip").json()['origin']
print(f"[INFO] Normal IP: {normal_ip}")

# Check IP via Tor SOCKS5
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
tor_ip = requests.get("https://httpbin.org/ip", proxies=proxies).json()['origin']
print(f"[INFO] Tor IP: {tor_ip}")
