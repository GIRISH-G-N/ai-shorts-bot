"""
upload_instagram.py
Uploads video reel to Instagram.
Credentials from .env — never hardcode passwords.
"""

import os
import sys
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

IG_USERNAME  = os.getenv("IG_USERNAME")
IG_PASSWORD  = os.getenv("IG_PASSWORD")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CONTENT_NICHE = os.getenv("CONTENT_NICHE", "dark_truth")

slot = sys.argv[1] if len(sys.argv) > 1 else "morning"
VIDEO_PATH   = Path(f"assets/{slot}/short_{slot}.mp4")
SESSION_FILE = "ig_session.json"
SCRIPT_PATH  = "output/script.txt"

if not IG_USERNAME or not IG_PASSWORD:
    raise RuntimeError("❌ IG_USERNAME and IG_PASSWORD must be set in .env")

# ==============================
# GENERATE CAPTION via Claude
# ==============================
def generate_caption():
    script = ""
    if os.path.exists(SCRIPT_PATH):
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            script = f.read().strip()

    if not ANTHROPIC_API_KEY or not script:
        return f"The truth nobody tells you. 🔥 #motivation #reels #shorts #{slot}"

    prompt = f"""Write an Instagram Reels caption for this video script:
"{script}"

Rules:
- 1-2 sentences MAX
- End with 3-5 relevant hashtags
- One emoji maximum — only if it genuinely fits
- No generic captions like "follow for more" or "drop a comment"
- Should feel like something a real person would post, not a bot
- Make it feel like a teaser that makes people want to watch

Return ONLY the caption text, nothing else."""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-opus-4-5",
        "max_tokens": 150,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body, timeout=20)
        r.raise_for_status()
        return r.json()["content"][0]["text"].strip()
    except Exception as e:
        print(f"⚠️ Caption generation failed: {e}")
        return f"The truth nobody tells you. 🔥 #motivation #reels"

# ==============================
# CHALLENGE HANDLER
# ==============================
def challenge_code_handler(username, choice):
    print(f"⚠️ Instagram verification needed for {username}")
    if choice == 0:
        return input("Enter SMS verification code: ")
    elif choice == 1:
        return input("Enter Email verification code: ")
    return False

# ==============================
# UPLOAD
# ==============================
def run_upload():
    from instagrapi import Client
    from instagrapi.exceptions import ChallengeRequired

    if not VIDEO_PATH.exists():
        print(f"❌ Video not found: {VIDEO_PATH}")
        return False

    caption = generate_caption()
    print(f"📝 Caption: {caption[:80]}...")

    cl = Client()
    cl.challenge_code_handler = challenge_code_handler
    cl.set_user_agent(
        "Instagram 269.1.0.18.110 Android (31/12; 480dpi; 1080x2219; samsung; SM-G991B; o1q; exynos2100; en_GB; 444303271)"
    )

    # ---- LOGIN ----
    try:
        if os.path.exists(SESSION_FILE):
            print("📂 Loading saved session...")
            cl.load_settings(SESSION_FILE)

        print(f"🔑 Logging in as {IG_USERNAME}...")
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Login successful")

    except ChallengeRequired as e:
        print("🛡️ Security challenge required...")
        cl.handle_exception(e)
    except Exception as e:
        print(f"⚠️ Session load failed, trying fresh login: {e}")
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(SESSION_FILE)

    # ---- UPLOAD ----
    print(f"🚀 Uploading Reel ({slot})...")
    try:
        media = cl.video_upload(path=VIDEO_PATH, caption=caption)
        print(f"✅ Reel posted! ID: {media.dict().get('pk')}")
        return True

    except Exception as e:
        err = str(e)
        print(f"❌ Upload failed: {err}")

        if "authorization" in err.lower() or "temporary" in err.lower():
            print("⏳ Rate limited — waiting 45s before retry...")
            time.sleep(45)
            try:
                media = cl.video_upload(path=VIDEO_PATH, caption=caption)
                print(f"✅ Retry successful! ID: {media.dict().get('pk')}")
                return True
            except Exception as e2:
                print(f"❌ Retry failed: {e2}")

        return False

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    import io
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    success = run_upload()
    sys.exit(0 if success else 1)
