"""
merge_video.py
Merges background video + voice + music.
Handles: cropping to voice length, audio ducking, proper export.
"""

import os
import sys
import random
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

slot = sys.argv[1] if len(sys.argv) > 1 else "morning"

VIDEO_PATH = "assets/videos/background.mp4"
VOICE_PATH = "assets/voice/voice.mp3"
MUSIC_DIR  = "assets/music"
OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_short.mp4")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# LOAD ASSETS
# ==============================
print("📂 Loading assets...")

if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"❌ Background video not found: {VIDEO_PATH}")
if not os.path.exists(VOICE_PATH):
    raise FileNotFoundError(f"❌ Voice not found: {VOICE_PATH}")

video = VideoFileClip(VIDEO_PATH)
voice = AudioFileClip(VOICE_PATH)

# ==============================
# TRIM VIDEO TO VOICE LENGTH + 0.5s buffer
# ==============================
target_duration = voice.duration + 0.5

if video.duration < target_duration:
    # Loop video if too short
    from moviepy.editor import concatenate_videoclips
    loops = int(target_duration / video.duration) + 1
    video = concatenate_videoclips([video] * loops)

video = video.subclip(0, target_duration)

# ==============================
# PICK MUSIC
# ==============================
music_files = [
    os.path.join(MUSIC_DIR, f)
    for f in os.listdir(MUSIC_DIR)
    if f.lower().endswith(".mp3")
]

if not music_files:
    print("⚠️ No music found — exporting without background music")
    final_audio = voice.volumex(1.0)
    music_name = "none"
else:
    music_path = random.choice(music_files)
    music_name = os.path.basename(music_path)
    music = AudioFileClip(music_path)
    music = music.subclip(0, min(target_duration, music.duration))

    # Voice at full volume, music ducked to 8%
    final_audio = CompositeAudioClip([
        voice.volumex(1.0),
        music.volumex(0.08)
    ])

# ==============================
# EXPORT
# ==============================
print("🎬 Rendering final video...")
final_video = video.set_audio(final_audio)

final_video.write_videofile(
    OUTPUT_PATH,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    preset="fast",
    threads=4,
    logger=None  # Suppress verbose moviepy logs
)

print(f"✅ Video rendered")
print(f"🎵 Music: {music_name}")
print(f"⏱️ Duration: {target_duration:.1f}s")
print(f"📁 Output: {OUTPUT_PATH}")
