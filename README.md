# LinkedIn AI Auto-Poster (Professional Edition)

An automated, modular system that researches, generates, and posts AI-related content to LinkedIn. (Scheduled automation disabled).

## 📁 Project Structure
```text
linkdin/
├── config/
│   ├── .env                # API keys and credentials
│   └── config.py           # Centralized configuration and templates
├── core/
│   ├── scheduler.py        # 🚀 Manual Trigger / Run-once entry
│   ├── automation.py       # 🚀 Pipeline orchestrator
│   ├── fetcher.py          # 🔍 News & Research fetcher
│   ├── summarizer.py       # ✍️ AI Content generator (Groq)
│   ├── formatter.py        # 📄 Content styling & formatting
│   ├── image_gen.py        # 🎨 AI Image generator (Pollinations)
│   ├── publisher.py        # 🚀 LinkedIn API integration
│   └── logger.py           # 📝 Structured logging & duplicate protection
├── data/
│   ├── outputs/            # Generated images
│   └── post_log.jsonl      # Structured post history
├── logs/
│   ├── success.log         # Detailed success history
│   └── error.log           # Debugging and failure logs
├── README.md               # You are here
└── requirements.txt        # Python dependencies
```

## 📅 Daily Topics
- **Mon**: AI Tech & Tools
- **Tue**: AI Healthcare
- **Wed**: AI Finance
- **Thu**: Business Automation
- **Fri**: Research & Innovation
- **Sat**: Personal Health & Wearables
- **Sun**: Weekly Trends Recap

## 🛠️ Setup & Usage
1. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. **Configure Credentials**:
   Edit `config/.env` with your API keys.
3. **Manual Trigger**:
   ```bash
   python core/scheduler.py
   ```
4. **Advanced Manual Trigger**:
   - Preview today's post (Dry Run): `python core/automation.py --test`
   - Trigger a specific day (0=Mon, 6=Sun): `python core/automation.py 1`
   - Force immediate post: `python core/automation.py`

## 🛡️ Key Features
- **Pro SaaS Dashboard**: Completely revamped dark-themed UI with KPI metrics and live side-by-side preview.
- **Pexels Integration**: High-quality professional stock images automatically sourced with required attribution.
- **Modular Design**: Each stage is isolated for easy maintenance.
- **Duplicate Protection**: Uses topic hashes and SQLite tracking to avoid reposting.
- **Failure Handling**: 3x retries on LinkedIn API failures with automated error logging.
- **Structured Logs**: All actions are logged in JSON for future analytics.
