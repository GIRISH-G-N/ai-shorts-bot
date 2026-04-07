"""
run_pipeline.py
Single unified pipeline runner. Replaces run_morning.py and run_evening.py.

Usage:
    python run_pipeline.py morning
    python run_pipeline.py evening
"""

import sys
import shutil
from pathlib import Path
from safe_run import safe_run

# ==============================
# SLOT
# ==============================
slot = sys.argv[1] if len(sys.argv) > 1 else "morning"

if slot not in ("morning", "evening"):
    print("❌ Usage: python run_pipeline.py morning|evening")
    sys.exit(1)

OUTPUT_FILE = Path("output/final_short_captioned.mp4")
DEST_DIR    = Path(f"assets/{slot}")
DEST_FILE   = DEST_DIR / f"short_{slot}.mp4"

DEST_DIR.mkdir(parents=True, exist_ok=True)

print(f"\n{'='*50}")
print(f"  {'🌅' if slot == 'morning' else '🌙'} {slot.upper()} PIPELINE STARTING")
print(f"{'='*50}\n")

# ==============================
# STEP 1: Generate script
# ==============================
if not safe_run("script_generator.py", slot):
    print("🚨 Pipeline stopped: script generation failed")
    sys.exit(1)

# ==============================
# STEP 2: Generate voice
# ==============================
if not safe_run("voice_generator.py", slot):
    print("🚨 Pipeline stopped: voice generation failed")
    sys.exit(1)

# ==============================
# STEP 3: Fetch background video
# ==============================
if not safe_run("fetch_pexels.py", slot):
    print("🚨 Pipeline stopped: video fetch failed")
    sys.exit(1)

# ==============================
# STEP 4: Merge video + voice + music
# ==============================
if not safe_run("merge_video.py", slot):
    print("🚨 Pipeline stopped: video merge failed")
    sys.exit(1)

# ==============================
# STEP 5: Add captions
# ==============================
if not safe_run("auto_captions.py", slot):
    print("⚠️ Captions failed — continuing with uncaptioned video")
    # Fallback: use non-captioned video
    shutil.copy("output/final_short.mp4", str(OUTPUT_FILE))

# ==============================
# STEP 6: Move final video to slot folder
# ==============================
if not OUTPUT_FILE.exists():
    print("🚨 Pipeline stopped: final output video not found")
    sys.exit(1)

if DEST_FILE.exists():
    DEST_FILE.unlink()

shutil.move(str(OUTPUT_FILE), str(DEST_FILE))
print(f"\n🎬 Final video saved: {DEST_FILE}")

# ==============================
# STEP 7: Upload to YouTube
# ==============================
print("\n📤 Uploading to YouTube...")
yt_success = safe_run("youtube_upload.py", slot, retries=2, wait=15)
if not yt_success:
    print("⚠️ YouTube upload failed — video saved locally")

# ==============================
# STEP 8: Upload to Instagram
# ==============================
print("\n📸 Uploading to Instagram...")
ig_success = safe_run("upload_instagram.py", slot, retries=2, wait=20)
if not ig_success:
    print("⚠️ Instagram upload failed — video saved locally")

# ==============================
# DONE
# ==============================
print(f"\n{'='*50}")
print(f"  ✅ {slot.upper()} PIPELINE COMPLETE")
print(f"  📁 Video : {DEST_FILE}")
print(f"  📺 YouTube: {'✅' if yt_success else '❌'}")
print(f"  📸 Instagram: {'✅' if ig_success else '❌'}")
print(f"{'='*50}\n")
