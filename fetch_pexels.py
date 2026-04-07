"""
fetch_pexels.py
Fetches background video from Pexels.
Smarter query selection based on content niche + visual quality filtering.
"""

import requests
import os
import random
import sys
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")
CONTENT_NICHE = os.getenv("CONTENT_NICHE", "dark_truth")
slot = sys.argv[1] if len(sys.argv) > 1 else "morning"

if not API_KEY:
    raise RuntimeError("PEXELS_API_KEY not found in .env")

HEADERS = {"Authorization": API_KEY}

# ==============================
# VISUAL THEMES PER NICHE
# These are carefully picked to MATCH the content emotionally
# ==============================
NICHE_QUERIES = {
    "dark_truth": [
        "person walking alone city night",
        "empty road rain night",
        "lone figure urban night",
        "rainy window city lights",
        "person thinking alone coffee",
        "empty street neon lights",
        "silhouette city sunset",
        "dark city timelapse night",
    ],
    "gen_z_wealth": [
        "person working laptop cafe",
        "city timelapse sunrise",
        "hands typing laptop night",
        "young entrepreneur working",
        "coffee laptop morning work",
        "busy city street hustle",
        "stock chart investment",
        "person reading finance book",
    ],
    "silent_grind": [
        "person training alone gym",
        "early morning workout",
        "person studying late night",
        "empty gym dark morning",
        "running alone street night",
        "person working desk night",
        "solitude focus work",
        "lone runner city morning",
    ],
    "uncomfortable": [
        "person scrolling phone night",
        "crowd people phone screens",
        "person alone party",
        "social media phone addiction",
        "person staring window thinking",
        "empty apartment city view",
        "busy street alone feeling",
        "person mirror reflection",
    ]
}

# Fallback queries if niche queries return nothing
FALLBACK_QUERIES = [
    "city night cinematic",
    "urban night atmosphere",
    "cinematic dark street",
]

# ==============================
# SEARCH
# ==============================
def search_videos(query):
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 40,
        "size": "medium"
    }
    r = requests.get(
        "https://api.pexels.com/videos/search",
        headers=HEADERS,
        params=params,
        timeout=30
    )
    r.raise_for_status()
    return r.json().get("videos", [])

# ==============================
# QUALITY FILTER
# Prefers: 15-35s duration, HD resolution
# ==============================
def filter_quality(videos):
    quality = []
    for v in videos:
        duration = v.get("duration", 0)
        if 15 <= duration <= 35:
            # Check if it has at least one HD mp4
            mp4s = [f for f in v["video_files"] if f.get("file_type") == "video/mp4"]
            hd = [f for f in mp4s if f.get("width", 0) >= 1080]
            if hd:
                quality.append(v)
    return quality

# ==============================
# MAIN FETCH
# ==============================
queries = NICHE_QUERIES.get(CONTENT_NICHE, NICHE_QUERIES["dark_truth"])
random.shuffle(queries)

all_queries = queries + FALLBACK_QUERIES

videos = []
used_query = None

for q in all_queries:
    print(f"🔎 Trying: {q}")
    results = search_videos(q)
    filtered = filter_quality(results)
    if filtered:
        videos = filtered
        used_query = q
        print(f"✅ Found {len(filtered)} quality videos")
        break
    elif results:
        print(f"⚠️ Found {len(results)} videos but none passed quality filter")

if not videos:
    print("⚠️ Relaxing quality filter...")
    for q in all_queries[:3]:
        results = search_videos(q)
        if results:
            videos = [v for v in results if 10 <= v.get("duration", 0) <= 60]
            used_query = q
            if videos:
                break

if not videos:
    raise RuntimeError("❌ Could not find any suitable video from Pexels")

# ==============================
# SELECT & DOWNLOAD
# ==============================
selected = random.choice(videos)

mp4s = [f for f in selected["video_files"] if f.get("file_type") == "video/mp4"]
mp4s.sort(key=lambda x: x.get("width", 0), reverse=True)
video_url = mp4s[0]["link"]

os.makedirs("assets/videos", exist_ok=True)

print(f"⬇️ Downloading video ({selected.get('duration')}s)...")
video_data = requests.get(video_url, timeout=60).content

with open("assets/videos/background.mp4", "wb") as f:
    f.write(video_data)

print(f"✅ Video downloaded")
print(f"🔎 Query: {used_query}")
print(f"⏱️ Duration: {selected.get('duration')}s")
print(f"📁 Saved: assets/videos/background.mp4")
