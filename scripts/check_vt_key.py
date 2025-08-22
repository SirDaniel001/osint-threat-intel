import requests
import os
from dotenv import load_dotenv

load_dotenv()  # this loads .env into environment variables

API_KEY = os.getenv("VT_API_KEY")
if not API_KEY:
    print("[!] No API key found. Did you set VT_API_KEY in .env?")
    exit()

url = "https://www.virustotal.com/api/v3/users/me"
headers = {"x-apikey": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("[+] API key is valid!")
    print(response.json())
else:
    print(f"[!] Invalid API key or expired. Status: {response.status_code}")
    print(response.text)
