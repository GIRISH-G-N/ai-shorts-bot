"""
voice_generator.py
Generates voiceover from script using edge-tts.
Multiple voice options — pick the one that fits your vibe.
"""

import asyncio
import edge_tts
import os
import sys
from dotenv import load_dotenv

load_dotenv()

slot = sys.argv[1] if len(sys.argv) > 1 else "morning"

# ==============================
# VOICE OPTIONS (comment/uncomment to switch)
# ==============================
# Deep, calm, authoritative — good for dark truth / wealth
VOICE = "en-US-GuyNeural"

# Younger, energetic — good for Gen Z content
# VOICE = "en-US-AndrewNeural"

# British, sharp — good for uncomfortable truths
# VOICE = "en-GB-RyanNeural"

# ==============================
# RATE BY SLOT
# ==============================
RATE = "-8%" if slot == "evening" else "-3%"  # Slightly slower at night = more reflective

# ==============================
# MAIN
# ==============================
async def main():
    script_path = "output/script.txt"

    if not os.path.exists(script_path):
        raise FileNotFoundError("❌ output/script.txt not found — run script_generator.py first")

    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read().strip()

    if not script:
        raise ValueError("❌ Script is empty")

    os.makedirs("assets/voice", exist_ok=True)
    output_path = "assets/voice/voice.mp3"

    communicate = edge_tts.Communicate(
        text=script,
        voice=VOICE,
        rate=RATE,
        volume="+0%",
        pitch="-5Hz"  # Slightly deeper = more cinematic
    )

    await communicate.save(output_path)

    print(f"🎙️ Voice generated | Voice: {VOICE} | Rate: {RATE}")
    print(f"📝 Script: {script[:80]}...")
    print(f"📁 Saved: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
