"""
auto_captions.py
Adds word-synced captions to the final video using Whisper.
Clean, centered, bold, with a pop animation.
"""

# PIL PATCH (must be first)
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import whisper
import numpy as np
from PIL import ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

VIDEO_IN  = "output/final_short.mp4"
VIDEO_OUT = "output/final_short_captioned.mp4"
FONT_PATH = "assets/fonts/Montserrat-Bold.ttf"

# ==============================
# LOAD
# ==============================
print("📂 Loading video...")
video = VideoFileClip(VIDEO_IN)

print("🧠 Running Whisper transcription...")
model = whisper.load_model("base")
result = model.transcribe(VIDEO_IN, word_timestamps=True, fp16=False, verbose=False)

# ==============================
# CAPTION STYLE CONFIG
# ==============================
FONT_SIZE    = 64
STROKE_WIDTH = 3
TEXT_Y_POS   = 0.72  # 72% down the screen — safe for Shorts
MAX_WORDS    = 2     # Words per caption pop

# ==============================
# RENDER TEXT FRAME
# ==============================
def render_text(text, scale=1.0):
    size = int(FONT_SIZE * scale)
    try:
        font = ImageFont.truetype(FONT_PATH, size)
    except Exception:
        font = ImageFont.load_default()

    dummy = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0, 0), text, font=font, stroke_width=STROKE_WIDTH)

    w = bbox[2] - bbox[0] + 60
    h = bbox[3] - bbox[1] + 40

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text(
        (30, 20), text, font=font,
        fill=(255, 255, 255, 255),
        stroke_width=STROKE_WIDTH,
        stroke_fill=(0, 0, 0, 230)
    )

    rgb   = np.array(img.convert("RGB"))
    alpha = np.array(img.split()[-1]) / 255.0
    return rgb, alpha

# ==============================
# BUILD CAPTION CLIPS
# ==============================
layers = [video]
y_pos = int(video.h * TEXT_Y_POS)

for seg in result["segments"]:
    if "words" not in seg:
        continue

    words = seg["words"]
    buffer = []
    start_time = None

    def flush_buffer(buf, t_start, t_end):
        if not buf or t_start is None:
            return
        duration = max(0.08, t_end - t_start)
        text = " ".join(buf).upper()

        def make_frame(t, txt=text):
            scale = 0.92 + 0.08 * min(t / 0.1, 1.0)
            return render_text(txt, scale)[0]

        def make_mask(t, txt=text):
            scale = 0.92 + 0.08 * min(t / 0.1, 1.0)
            return render_text(txt, scale)[1]

        clip = (
            ImageClip(make_frame(0))
            .set_make_frame(make_frame)
            .set_mask(ImageClip(make_mask(0), ismask=True).set_make_frame(make_mask))
            .set_start(t_start)
            .set_duration(duration)
            .set_position(("center", y_pos))
        )
        layers.append(clip)

    for w in words:
        word = w["word"].strip()
        if not word:
            continue

        if start_time is None:
            start_time = w["start"]

        buffer.append(word)

        if len(buffer) == MAX_WORDS:
            flush_buffer(buffer, start_time, w["end"])
            buffer = []
            start_time = None

    # Leftover words
    if buffer:
        flush_buffer(buffer, start_time, seg["end"])

# ==============================
# EXPORT
# ==============================
print("🎬 Compositing captions...")
final = CompositeVideoClip(layers).set_audio(video.audio)

final.write_videofile(
    VIDEO_OUT,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    preset="fast",
    threads=4,
    logger=None
)

print("✅ Captions added")
print(f"📁 Output: {VIDEO_OUT}")
