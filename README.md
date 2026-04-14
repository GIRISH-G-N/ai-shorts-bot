# 🔥 AI Auto Shorts — Rewritten

Fully automated YouTube Shorts + Instagram Reels pipeline. Generates unique scripts using Groq AI (FREE), syncs voice + cinematic visuals + captions, and uploads automatically.

---

## 📁 Project Structure

```
project/
├── .env                    ← Your API keys (never commit this)
├── .env.example            ← Template to copy from
├── run_pipeline.py         ← MAIN RUNNER
├── script_generator.py     ← Groq AI script generation (FREE)
├── voice_generator.py      ← Text-to-speech via edge-tts
├── fetch_pexels.py         ← Background video from Pexels
├── merge_video.py          ← Combines video + voice + music
├── auto_captions.py        ← Word-synced captions via Whisper
├── youtube_upload.py       ← Upload + schedule to YouTube
├── upload_instagram.py     ← Upload Reel to Instagram
├── auto_music.py           ← Random background track picker
├── safe_run.py             ← Retry wrapper for all scripts
├── moviepy_config.py       ← ImageMagick path config
├── assets/
│   ├── music/              ← DROP YOUR MP3 FILES HERE
│   ├── fonts/Montserrat-Bold.ttf
│   ├── videos/
│   └── voice/
├── output/
├── assets/morning/
└── assets/evening/
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install requests python-dotenv edge-tts moviepy openai-whisper instagrapi google-auth-oauthlib google-api-python-client Pillow
```

### 2. Set up your .env
Copy .env.example to .env and fill in:
```env
PEXELS_API_KEY=your_key
GROQ_API_KEY=your_key
IG_USERNAME=your_ig_handle
IG_PASSWORD=your_ig_password
CONTENT_NICHE=dark_truth
```
Get your keys:
- Pexels: https://www.pexels.com/api/
- Groq (FREE — no card): https://console.groq.com

### 3. Add music
Drop MP3 files into assets/music/
Free sources: Pixabay Music, Uppbeat, YouTube Audio Library

### 4. Add font
Download Montserrat Bold from Google Fonts → save as assets/fonts/Montserrat-Bold.ttf

### 5. YouTube auth (one time only)
```bash
python youtube_upload.py morning
```

---

## 🚀 Running
```bash
python run_pipeline.py morning
python run_pipeline.py evening
```

---

## 🎯 Content Niches

| Niche | What it posts | Best for |
|---|---|---|
| dark_truth | Uncomfortable facts about life, people, success | High shareability |
| gen_z_wealth | Practical money knowledge for 18-25s | Educational, loyal audience |
| silent_grind | Building alone without external validation | Deep niche, very engaged |
| uncomfortable | Social media, self-deception, modern life truths | Viral potential |

---

## 🤖 AI Script Generation (FREE)

This project uses Groq API — completely free, no credit card needed.
- 100% free forever
- Super fast (faster than ChatGPT)
- Uses Llama 3 model — natural sounding scripts
- 30 requests/minute free limit

Get your free key at: console.groq.com

---

## 🖥️ Deploy to Server (Run 24/7 Without Your Laptop)

### 🥇 Option 1 — DigitalOcean (Recommended)
Cost: $12/month — FREE for students with GitHub Student Pack ($200 credits = 16 months)

Step 1 — Create Droplet:
1. Sign up at digitalocean.com
2. Create Droplet → Ubuntu 24.04
3. Plan: $12/month (2GB RAM)
4. Region: Bangalore (India)
5. Authentication: Password
6. Click Create

Step 2 — Connect:
Click "Launch Droplet Console" in dashboard

Step 3 — Install dependencies:
```bash
apt update && apt upgrade -y
apt install python3 python3-pip git ffmpeg imagemagick -y
pip3 install requests python-dotenv edge-tts moviepy openai-whisper instagrapi google-auth-oauthlib google-api-python-client Pillow --break-system-packages
```

Step 4 — Clone repo:
```bash
git clone https://github.com/YOURUSERNAME/ai-shorts-bot.git
cd ai-shorts-bot
```

Step 5 — Create .env:
```bash
nano .env
```
Add your keys, save with CTRL+X → Y → Enter

Step 6 — Upload assets via FileZilla:
Download FileZilla → connect with server IP + password → upload:
- assets/music/ folder
- assets/fonts/Montserrat-Bold.ttf
- token.pickle (YouTube auth)

Step 7 — Set up cron jobs:
```bash
mkdir -p logs
crontab -e
```
Add:
```
0 7 * * * cd /root/ai-shorts-bot && python3 run_pipeline.py morning >> logs/morning.log 2>&1
0 19 * * * cd /root/ai-shorts-bot && python3 run_pipeline.py evening >> logs/evening.log 2>&1
```

Step 8 — Check logs:
```bash
tail -f logs/morning.log
```

Step 9 — Update code after changes:
```bash
cd ai-shorts-bot && git pull
```

---

### 🎓 GitHub Student Pack — Get DigitalOcean FREE
1. Go to education.github.com/pack
2. Verify with college email
3. Find DigitalOcean → claim $200 credits

---

### Option 2 — Railway.app
Cost: $5 free/month, no card needed
1. railway.app → New Project → Deploy from GitHub
2. Add environment variables
3. Add cron: 0 7 * * * python run_pipeline.py morning

---

### Option 3 — Oracle Cloud (Free Forever)
1. cloud.oracle.com
2. VM.Standard.A1.Flex → 4 CPU + 24GB RAM (free tier)

---

### Which one to pick?

| Option | Cost | RAM | Best for |
|---|---|---|---|
| DigitalOcean + Student Pack | Free 16 months | 2GB ✅ | ✅ Best overall |
| Railway.app | $5/month | Enough | Quick setup |
| Oracle Cloud | Free forever | 1GB ⚠️ | Patient people |
| Laptop | Electricity | Your RAM | ❌ Not sustainable |

---

## 🔧 Customizing Voice
```python
VOICE = "en-US-GuyNeural"      # Deep, calm
VOICE = "en-US-AndrewNeural"   # Younger, energetic
VOICE = "en-GB-RyanNeural"     # British, sharp
```

---

## 🐛 Common Issues

**No module named X** → pip install X

**Captions not showing** → Check assets/fonts/Montserrat-Bold.ttf exists

**Instagram login failing** → Delete ig_session.json and retry

**YouTube token expired** → Delete token.pickle, run python youtube_upload.py morning

**Pexels bad videos** → Edit NICHE_QUERIES in fetch_pexels.py

**Server out of memory** → Upgrade to 2GB RAM minimum

---

## 💡 Pro Tips

1. Test scripts first: python script_generator.py morning
2. Check voice: python voice_generator.py morning → listen to assets/voice/voice.mp3
3. Pick one niche, run 30 days, check analytics before switching
4. Update server after code changes: cd ai-shorts-bot && git pull
