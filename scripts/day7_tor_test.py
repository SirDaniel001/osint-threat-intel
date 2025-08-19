import requests
import json


def safe_get_json(url, proxies=None):
    """
    Safely fetch JSON from a URL, with optional proxies.
    Returns {} if request fails or response is invalid.
    """
    try:
        resp = requests.get(url, proxies=proxies, timeout=10)
        resp.raise_for_status()  # catch HTTP errors
        return resp.json()       # parse JSON
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"⚠️ Error fetching {url} (proxies={proxies}): {e}")
        return {}


if __name__ == "__main__":
    # Check IP without Tor
    normal_ip_data = safe_get_json("https://httpbin.org/ip")
    if "origin" in normal_ip_data:
        print(f"[INFO] Normal IP: {normal_ip_data['origin']}")
    else:
        print("❌ Could not fetch Normal IP")

    # Check IP via Tor SOCKS5
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    }
    tor_ip_data = safe_get_json("https://httpbin.org/ip", proxies=proxies)
    if "origin" in tor_ip_data:
        print(f"[INFO] Tor IP: {tor_ip_data['origin']}")
    else:
        print("❌ Could not fetch Tor IP (is Tor running on port 9050?)")
