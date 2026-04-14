"""
script_generator.py
Generates unique short-form video scripts using Groq API (FREE).
Niche: Dark Truth / Gen Z Wealth / Silent Grind / Uncomfortable Facts
"""

import os
import sys
import json
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HISTORY_FILE = "script_history.json"
CONTENT_NICHE = os.getenv("CONTENT_NICHE", "dark_truth")

slot = sys.argv[1] if len(sys.argv) > 1 else "morning"

# ==============================
# NICHE PROMPTS
# ==============================
NICHE_PROMPTS = {
    "dark_truth": """
You create short-form video scripts for YouTube Shorts and Instagram Reels.
The niche is "Dark Truths" — uncomfortable facts about life, money, success, and people
that most people know deep down but nobody says out loud.

Rules:
- 3-4 sentences MAX. Around 30-45 words total.
- First sentence is a BRUTAL, uncomfortable hook. Not cheesy. Not generic.
- Second sentence adds the painful detail or context.
- Third sentence is the real insight — what the person should actually do or realize.
- Optional fourth: short punchy closer that sticks in the head.
- NO hashtags, NO emojis, NO "follow for more", NO clichés like "grind harder" or "believe in yourself"
- Sound like a real person who figured something out, not a motivational poster
- Vary the topics: sometimes about friendships, sometimes money, sometimes time, sometimes identity
- NEVER repeat the same topic twice in a row

Current slot: {slot}
""",

    "gen_z_wealth": """
You create short-form video scripts for YouTube Shorts and Instagram Reels.
The niche is practical wealth knowledge for Gen Z (18-25 year olds).
Real information, not fluff. Things school never taught them.

Rules:
- 3-4 sentences MAX. Around 35-50 words total.
- Hook: a surprising money fact or statistic that makes them stop scrolling
- Middle: the actual useful information explained simply
- End: one clear action they can take TODAY
- NO generic motivation. Only real, actionable, specific information.
- Topics: credit scores, compound interest, index funds, salary negotiation, tax basics,
  side income, inflation, investing early, debt traps, spending psychology
- Sound like a smart older friend explaining money, not a finance bro

Current slot: {slot}
""",

    "silent_grind": """
You create short-form video scripts for YouTube Shorts and Instagram Reels.
The niche is "Silent Grind" — for people who are building something quietly,
without showing off, without external validation.

Rules:
- 3-4 sentences MAX. Around 30-45 words total.
- Hook: something that resonates deeply with someone building alone
- Middle: the uncomfortable truth about the process
- End: the payoff or reframe that makes it worth it
- Tone: calm, confident, like someone 5 years ahead of them talking back
- NO hype, NO "you got this bro" energy. Real and grounded.
- Topics: loneliness of the process, dealing with doubt, delayed results,
  people not understanding, choosing work over social life, identity shifts

Current slot: {slot}
""",

    "uncomfortable": """
You create short-form video scripts for YouTube Shorts and Instagram Reels.
The niche is uncomfortable truths about modern life — social media, relationships,
careers, self-deception, and the gap between who people are and who they pretend to be.

Rules:
- 3-4 sentences MAX. Around 30-45 words total.
- Hook: call out something specific that people do but won't admit
- Middle: why they actually do it (the real psychology)
- End: the honest alternative or reframe
- Tone: direct, a little cold, not preachy — like a doctor giving a diagnosis
- NO toxic positivity. NO victim blaming. Just honest observations.
- Topics: doom scrolling, comparison culture, performative productivity,
  people pleasing, avoiding hard conversations, identity tied to output

Current slot: {slot}
"""
}

# ==============================
# HISTORY SYSTEM
# ==============================
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {"hashes": [], "last_topics": []}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def is_duplicate(script, history):
    h = hashlib.sha256(script.encode()).hexdigest()
    return h in history["hashes"], h

# ==============================
# GROQ API CALL (FREE)
# ==============================
def call_groq(prompt):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set in .env")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-8b-8192",  # Free, fast, great quality
        "max_tokens": 300,
        "temperature": 0.9,  # Higher = more creative and varied
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()

# ==============================
# GENERATE SCRIPT
# ==============================
def generate_script():
    history = load_history()

    niche_template = NICHE_PROMPTS.get(CONTENT_NICHE, NICHE_PROMPTS["dark_truth"])
    prompt = niche_template.replace("{slot}", slot)

    last_topics = history.get("last_topics", [])
    if last_topics:
        prompt += f"\n\nDo NOT write about these recently used topics: {', '.join(last_topics[-3:])}"

    prompt += "\n\nWrite ONE script now. Output ONLY the script text, nothing else. No quotes, no labels, no explanations."

    for attempt in range(3):
        script = call_groq(prompt)
        script = script.strip().strip('"').strip("'")

        is_dup, hash_id = is_duplicate(script, history)
        if not is_dup:
            history["hashes"].append(hash_id)

            topic_key = " ".join(script.split()[:4])
            history.setdefault("last_topics", []).append(topic_key)
            history["last_topics"] = history["last_topics"][-10:]

            save_history(history)

            os.makedirs("output", exist_ok=True)
            with open("output/script.txt", "w", encoding="utf-8") as f:
                f.write(script)

            return script

        print(f"⚠️ Duplicate detected, retrying... ({attempt + 1}/3)")

    raise RuntimeError("Failed to generate unique script after 3 attempts")

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    script = generate_script()
    print("\n🧠 SCRIPT GENERATED:\n")
    print(script)
    print(f"\n📁 Saved to output/script.txt")
