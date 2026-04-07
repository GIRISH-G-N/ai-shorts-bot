# 🔥 AI Auto Shorts — Rewritten

Fully automated YouTube Shorts + Instagram Reels pipeline.
Generates unique scripts using Claude AI, syncs voice + cinematic visuals + captions, and uploads automatically.

---

## 📁 Project Structure

```
project/
├── .env                    ← Your API keys (never commit this)
├── .env.example            ← Template to copy from
│
├── run_pipeline.py         ← MAIN RUNNER (replaces run_morning + run_evening)
├── script_generator.py     ← Claude AI script generation
├── voice_generator.py      ← Text-to-speech via edge-tts
├── fetch_pexels.py         ← Background video from Pexels
├── merge_video.py          ← Combines video + voice + music
├── auto_captions.py        ← Word-synced captions via Whisper
├── youtube_upload.py       ← Upload + schedule to YouTube
├── upload_instagram.py     ← Upload Reel to Instagram
├── auto_music.py           ← Random background track picker
├── safe_run.py             ← Retry wrapper for all scripts
├── moviepy_config.py       ← ImageMagick path config
│
├── assets/
│   ├── music/              ← DROP YOUR MP3 FILES HERE
│   ├── fonts/
│   │   └── Montserrat-Bold.ttf   ← Required for captions
│   ├── videos/             ← Auto-filled by fetch_pexels.py
│   └── voice/              ← Auto-filled by voice_generator.py
│
├── output/                 ← Intermediate files
├── assets/morning/         ← Final morning video lands here
└── assets/evening/         ← Final evening video lands here
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install anthropic requests python-dotenv edge-tts moviepy openai-whisper instagrapi google-auth-oauthlib google-api-python-client Pillow
```

### 2. Set up your .env

Copy `.env.example` to `.env` and fill in:

```env
PEXELS_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
IG_USERNAME=your_ig_handle
IG_PASSWORD=your_ig_password
CONTENT_NICHE=dark_truth
```

Get your keys:
- Pexels: https://www.pexels.com/api/
- Anthropic: https://console.anthropic.com/

### 3. Add music

Drop MP3 files into `assets/music/`. The more variety the better.
Free sources: Pixabay Music, Uppbeat, YouTube Audio Library

### 4. Add font

Download Montserrat Bold from Google Fonts → save as `assets/fonts/Montserrat-Bold.ttf`

### 5. YouTube auth (one time)

Run once manually — it opens a browser for Google OAuth:
```bash
python youtube_upload.py morning
```
After that, `token.pickle` handles auth automatically.

---

## 🚀 Running

```bash
# Morning video
python run_pipeline.py morning

# Evening video
python run_pipeline.py evening
```

---

## 🎯 Content Niches

Change `CONTENT_NICHE` in `.env` to switch your channel angle:

| Niche | What it posts | Best for |
|---|---|---|
| `dark_truth` | Uncomfortable facts about life, people, success | High shareability |
| `gen_z_wealth` | Practical money knowledge for 18-25s | Educational, loyal audience |
| `silent_grind` | Building alone without external validation | Deep niche, very engaged |
| `uncomfortable` | Social media, self-deception, modern life truths | Viral potential |

---

## ⏰ Automating (so your laptop stays OFF)

### Option 1: Windows Task Scheduler (simplest)
1. Open Task Scheduler → Create Basic Task
2. Set trigger: Daily at 7:00 AM
3. Action: `python C:\path\to\run_pipeline.py morning`
4. Repeat for 7:00 PM evening

### Option 2: Railway.app (recommended — cloud, always on)
1. Push this folder to a GitHub repo (without .env)
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Add environment variables in Railway dashboard
4. Add a cron job: `0 7 * * * python run_pipeline.py morning`
5. Add another: `0 19 * * * python run_pipeline.py evening`

### Option 3: GitHub Actions (free but limited compute)
Good for light scripts, struggles with video processing.

---

## 🔧 Customizing Voice

In `voice_generator.py`, change the `VOICE` variable:

```python
VOICE = "en-US-GuyNeural"      # Deep, calm, authoritative
VOICE = "en-US-AndrewNeural"   # Younger, energetic
VOICE = "en-GB-RyanNeural"     # British, sharp
```

Run `edge-tts --list-voices` to see all options.

---

## 🐛 Common Issues

**"No module named X"** → `pip install X`

**Captions not showing** → Make sure `assets/fonts/Montserrat-Bold.ttf` exists

**Instagram login failing** → Delete `ig_session.json` and retry. Instagram sometimes requires verification on first login from a new device.

**YouTube token expired** → Delete `token.pickle` and run `python youtube_upload.py morning` manually to re-authenticate.

**Pexels returning bad videos** → Edit `NICHE_QUERIES` in `fetch_pexels.py` and add better search terms you've tested manually on pexels.com

---

## 💡 Pro Tips

1. **Curate your Pexels queries** — search manually on pexels.com first, find queries that return videos you like, then add those specific queries to `NICHE_QUERIES`

2. **Test scripts before running the full pipeline:**
   ```bash
   python script_generator.py morning
   cat output/script.txt
   ```

3. **Check voice quality before uploading:**
   ```bash
   python voice_generator.py morning
   # Listen to assets/voice/voice.mp3
   ```

4. **Switch niches gradually** — pick one niche, run it for 30 days, check analytics before switching
