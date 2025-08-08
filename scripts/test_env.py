import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch values
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_receiver = os.getenv("EMAIL_RECEIVER")

print("[TEST] Checking environment variables...")
print(f"EMAIL_SENDER: {email_sender}")
print(f"EMAIL_PASSWORD: {email_password}")
print(f"EMAIL_RECEIVER: {email_receiver}")
