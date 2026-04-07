"""
youtube_upload.py
Uploads video to YouTube with AI-generated title and description.
Schedules 20 minutes from now.
"""

import os
import sys
import pickle
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

SCOPES     = ["https://www.googleapis.com/auth/youtube.upload"]
slot       = sys.argv[1] if len(sys.argv) > 1 else "morning"
VIDEO_PATH = f"assets/{slot}/short_{slot}.mp4"
SCRIPT_PATH = "output/script.txt"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CONTENT_NICHE = os.getenv("CONTENT_NICHE", "dark_truth")

# ==============================
# LOAD SCRIPT
# ==============================
if not os.path.exists(SCRIPT_PATH):
    raise FileNotFoundError("❌ output/script.txt not found")

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    SCRIPT = f.read().strip()

# ==============================
# GENERATE TITLE + TAGS via Claude
# ==============================
def generate_youtube_meta(script, slot):
    if not ANTHROPIC_API_KEY:
        # Fallback if no API key
        first = script.split(".")[0].strip()[:70]
        return f"{first} #shorts", ["motivation", "mindset", "shorts"]

    prompt = f"""Given this short-form video script:
"{script}"

Generate YouTube metadata. Return ONLY a JSON object like this:
{{
  "title": "catchy title under 70 chars, no hashtags, hooks the viewer",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}

Rules for title:
- Must make someone want to click
- No clickbait lies, just compelling truth
- No emojis
- No generic phrases like "motivation" or "mindset"

Tags should be relevant niche hashtags without the # symbol.
"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-opus-4-5",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body, timeout=20)
        r.raise_for_status()
        import json, re
        text = r.json()["content"][0]["text"]
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return data.get("title", script[:70]), data.get("tags", [])
    except Exception as e:
        print(f"⚠️ Meta generation failed: {e}")

    first = script.split(".")[0].strip()[:70]
    return first, ["motivation", "mindset", "shorts", "discipline", "success"]

TITLE, TAGS = generate_youtube_meta(SCRIPT, slot)

HASHTAG_STR = " ".join(f"#{t}" for t in TAGS)

DESCRIPTION = f"""{SCRIPT}

{HASHTAG_STR} #shorts #youtubeshorts
""".strip()

publish_time = datetime.now(timezone.utc) + timedelta(minutes=20)

# ==============================
# AUTH
# ==============================
def get_youtube():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as f:
            creds = pickle.load(f)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)

# ==============================
# UPLOAD
# ==============================
def upload():
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"❌ Video not found: {VIDEO_PATH}")

    youtube = get_youtube()

    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_time.isoformat().replace("+00:00", "Z"),
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(VIDEO_PATH, resumable=True, chunksize=-1)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    print("✅ YouTube Upload Success")
    print(f"📺 Video ID : {response['id']}")
    print(f"📝 Title    : {TITLE}")
    print(f"⏰ Scheduled: {publish_time.strftime('%Y-%m-%d %H:%M UTC')}")

if __name__ == "__main__":
    print(f"🔐 Authenticating...")
    print(f"📤 Uploading [{slot.upper()}] video...")
    upload()
