# Handles loading secrets and configs
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# --- Google ---
# For GitHub Actions, the JSON content is passed as a string secret
#google_creds_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
#GOOGLE_CREDENTIALS = json.loads(google_creds_json_str) if #google_creds_json_str else None
#GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")

# --- Twitter ---
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# --- Facebook ---
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# --- gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- App Settings ---
TWITTER_CHAR_LIMIT = 280

