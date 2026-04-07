"""
auto_music.py
Picks a random background track from assets/music and copies it as bg_music.mp3.
Add your own MP3 files to assets/music/ — the more the better.
"""

import os
import random
import shutil

MUSIC_DIR    = "assets/music"
OUTPUT_MUSIC = os.path.join(MUSIC_DIR, "bg_music.mp3")

tracks = [
    f for f in os.listdir(MUSIC_DIR)
    if f.lower().endswith(".mp3") and f != "bg_music.mp3"
]

if not tracks:
    raise RuntimeError("❌ No MP3 files found in assets/music/ — add some tracks first")

selected = random.choice(tracks)
source   = os.path.join(MUSIC_DIR, selected)

shutil.copy(source, OUTPUT_MUSIC)

print(f"🎵 Selected track : {selected}")
print(f"📁 Saved as       : {OUTPUT_MUSIC}")
