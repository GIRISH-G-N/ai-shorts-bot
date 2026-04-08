# 🔥 AI Auto Shorts — Rewritten

Fully automated YouTube Shorts + Instagram Reels pipeline. Generates unique scripts using Claude AI, syncs voice + cinematic visuals + captions, and uploads automatically.

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

## ⏰ Automating on Your Laptop

### Windows Task Scheduler
1. Open Task Scheduler → Create Basic Task
2. Set trigger: Daily at 7:00 AM
3. Action: `python C:\path\to\run_pipeline.py morning`
4. Repeat for 7:00 PM evening

---

## 🖥️ Deploy to Server (Run 24/7 Without Your Laptop)

Running this on your laptop means keeping it on 24/7. A server handles everything automatically. Here are your best options:

---

### 🥇 Option 1 — DigitalOcean (Recommended)

**Cost:** $6-12/month — BUT free for students (see GitHub Student Pack below)

**Why DigitalOcean:**
- Simple and beginner friendly
- 2GB RAM handles everything including Whisper
- Runs 24/7 without your laptop
- $200 free credits with GitHub Student Pack = 16+ months free

#### Step 1 — Create a Droplet
1. Sign up at **digitalocean.com**
2. Create Droplet → choose **Ubuntu 22.04**
3. Plan: **$12/month (2GB RAM)** ← minimum for this project
4. Choose any region close to you
5. Add your SSH key or use password
6. Click Create

#### Step 2 — Connect to server
```bash
ssh root@YOUR_SERVER_IP
```

#### Step 3 — Install dependencies
```bash
apt update && apt upgrade -y
apt install python3 python3-pip git ffmpeg imagemagick -y
pip3 install anthropic requests python-dotenv edge-tts moviepy openai-whisper instagrapi google-auth-oauthlib google-api-python-client Pillow
```

#### Step 4 — Clone your repo
```bash
git clone https://github.com/YOURUSERNAME/ai-shorts-bot.git
cd ai-shorts-bot
```

#### Step 5 — Set up .env on server
```bash
nano .env
```
Paste your API keys, save with `CTRL+X → Y → Enter`

#### Step 6 — Add your assets
Upload your music files and font using SFTP (use FileZilla app — free):
- Host: your server IP
- Username: root
- Password: your server password
- Port: 22

Upload `assets/music/` and `assets/fonts/` folders.

#### Step 7 — YouTube auth on server (one time)
This is the tricky part — YouTube OAuth needs a browser. Do it locally first, then upload `token.pickle` to server via FileZilla.

#### Step 8 — Set up cron jobs (auto schedule)
```bash
crontab -e
```
Add these two lines:
```
0 7 * * * cd /root/ai-shorts-bot && python3 run_pipeline.py morning >> logs/morning.log 2>&1
0 19 * * * cd /root/ai-shorts-bot && python3 run_pipeline.py evening >> logs/evening.log 2>&1
```
Save → done. Now it runs every day at 7AM and 7PM automatically.

---

### 🎓 GitHub Student Pack — Get DigitalOcean FREE

If you're a student you can get **$200 free DigitalOcean credits** = 16+ months free.

1. Go to **education.github.com/pack**
2. Click Get Student Benefits
3. Verify with your college email or student ID
4. Wait 1-3 days for approval
5. Go to Student Pack → find DigitalOcean → claim $200 credits

---

### Option 2 — Railway.app

**Cost:** $5 free credits/month (no card needed)

Good for: quick setup, doesn't need much configuration

1. Go to **railway.app** → New Project → Deploy from GitHub
2. Connect your `ai-shorts-bot` repo
3. Add environment variables (same as your `.env`)
4. Add cron jobs:
   - `0 7 * * * python run_pipeline.py morning`
   - `0 19 * * * python run_pipeline.py evening`

**Limitation:** Free credits run out after ~1 month. Good for testing.

---

### Option 3 — Oracle Cloud (Always Free Forever)

**Cost:** Completely free forever

**The catch:** Hard to set up, and free tier gives only 1GB RAM which struggles with Whisper.

**If you want to try:**
1. Sign up at **cloud.oracle.com**
2. Create instance → shape: **VM.Standard.A1.Flex**
3. Set 4 CPU + 24GB RAM → this is the free tier
4. Follow same steps as DigitalOcean above after that

---

### ⚖️ Which one should you pick?

| Option | Cost | Difficulty | RAM | Recommended? |
|---|---|---|---|---|
| DigitalOcean + Student Pack | Free 16 months | Easy | 2GB ✅ | ✅ Best |
| Railway.app | ~$5/month | Easiest | Enough | ✅ Good start |
| Oracle Cloud | Free forever | Hard | 1GB ⚠️ | Only if patient |
| Your laptop | Electricity bill | None | Your RAM | ❌ Not sustainable |

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

**Instagram login failing** → Delete `ig_session.json` and retry

**YouTube token expired** → Delete `token.pickle` and run `python youtube_upload.py morning` manually

**Pexels returning bad videos** → Edit `NICHE_QUERIES` in `fetch_pexels.py` with better search terms

**Server running out of memory** → Upgrade to at least 2GB RAM droplet

---

## 💡 Pro Tips

1. **Curate your Pexels queries** — search manually on pexels.com first, find queries that return videos you like, then hardcode those in `NICHE_QUERIES`

2. **Test scripts before full pipeline:**
   ```bash
   python script_generator.py morning
   cat output/script.txt
   ```

3. **Check voice before uploading:**
   ```bash
   python voice_generator.py morning
   # Listen to assets/voice/voice.mp3
   ```

4. **Switch niches gradually** — pick one niche, run 30 days, check analytics before switching

5. **Check logs on server:**
   ```bash
   tail -f logs/morning.log
   ```
