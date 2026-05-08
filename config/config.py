import os
from pathlib import Path
from dotenv import load_dotenv

# Path Setup
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = DATA_DIR / "outputs"

# Ensure directories exist
for d in [CONFIG_DIR, DATA_DIR, LOGS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Load Environment Variables
load_dotenv(dotenv_path=CONFIG_DIR / ".env")

# API Keys
GROQ_API_KEY          = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY       = os.getenv("PEXELS_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN   = os.getenv("LINKEDIN_PERSON_URN")
SERPER_API_KEY        = os.getenv("SERPER_API_KEY")

# Scheduling & Topics
DAY_TOPICS = {
    0: { # Monday
        "name": "AI Tech & Tools",
        "label": "Latest updates in AI technology, tools, and new models",
        "rss_feeds": [
            "https://venturebeat.com/category/ai/feed/",
            "https://openai.com/news/rss/",
            "https://deepmind.google/blog/rss.xml",
            "https://huggingface.co/blog/feed.xml"
        ],
        "serper_queries": ["latest AI models releases 2026", "new AI tools this week"],
        "hashtags": ["AI", "AITools", "Innovation", "TechNews", "LLM"],
        "follow_cta": "Follow me for the latest AI technology updates and new model releases! 🤖",
    },
    1: { # Tuesday
        "name": "AI Healthcare",
        "label": "How AI is improving healthcare and medical systems",
        "rss_feeds": [
            "https://www.medgadget.com/feed",
            "https://healthcare-digital.com/rss",
            "https://www.nature.com/subjects/ai-in-medicine.rid"
        ],
        "serper_queries": ["AI in healthcare breakthroughs 2026", "medical AI systems improvements"],
        "hashtags": ["HealthTech", "AIHealthcare", "MedTech", "DigitalHealth"],
        "follow_cta": "Follow me for daily insights into how AI is transforming the medical world! 🏥",
    },
    2: { # Wednesday
        "name": "AI Finance",
        "label": "How AI is transforming finance, banking, and investments",
        "rss_feeds": [
            "https://www.finextra.com/rss/news",
            "https://www.americanbanker.com/feed",
            "https://finovate.com/feed/"
        ],
        "serper_queries": ["AI in finance trends 2026", "AI banking automation news"],
        "hashtags": ["FinTech", "AIFinance", "Banking", "Investment"],
        "follow_cta": "Follow me to stay ahead of the AI revolution in finance and banking! 💰",
    },
    3: { # Thursday
        "name": "AI Business Automation",
        "label": "How businesses are using AI to automate and scale operations",
        "rss_feeds": [
            "https://zapier.com/blog/feeds/latest/",
            "https://www.entrepreneur.com/topic/automation.rss",
            "https://techcrunch.com/category/enterprise/feed/"
        ],
        "serper_queries": ["AI business automation 2026 case studies", "enterprise AI automation trends"],
        "hashtags": ["Automation", "BusinessAI", "Scaling", "Productivity"],
        "follow_cta": "Follow me to learn how to scale your business with the power of AI automation! 🚀",
    },
    4: { # Friday
        "name": "AI Research & Innovation",
        "label": "Advanced AI research, innovations, and future technologies",
        "rss_feeds": [
            "https://arxiv.org/rss/cs.AI",
            "https://www.technologyreview.com/feed/",
            "https://ai.googleblog.com/feeds/posts/default"
        ],
        "serper_queries": ["advanced AI research papers 2026", "next-gen AI innovations"],
        "hashtags": ["AIResearch", "Innovation", "FutureTech", "DeepLearning"],
        "follow_cta": "Follow me for a deep dive into the most advanced AI research and future innovations! 🧪",
    },
    5: { # Saturday
        "name": "AI Personal Health",
        "label": "AI in personal health, fitness, and wearable devices",
        "rss_feeds": [
            "https://www.wareable.com/rss",
            "https://gadgetsandwearables.com/feed/",
            "https://www.fitbit.com/blog/rss"
        ],
        "serper_queries": ["AI fitness wearables news 2026", "AI personal health tracking innovations"],
        "hashtags": ["FitnessTech", "PersonalHealth", "Wearables", "AI"],
        "follow_cta": "Follow me for the latest updates on AI in fitness and personal health tech! ⌚",
    },
    6: { # Sunday
        "name": "AI News Weekly",
        "label": "Top AI news and hottest trends from the last 24 hours",
        "rss_feeds": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
            "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"
        ],
        "serper_queries": ["top AI news last 24 hours", "hottest AI trends this week summary"],
        "hashtags": ["AINews", "TechTrends", "WeeklyRecap", "AI"],
        "follow_cta": "Follow me for your essential weekly recap of the biggest AI news and trends! 📰",
    },
}

# Prompt Templates
LINKEDIN_BEST_PRACTICES = """
WHAT WORKS ON LINKEDIN RIGHT NOW (2025-2026 meta):
- Hook in line 1 BEFORE "...see more" cutoff
- Story-driven posts outperform pure information
- Short paragraphs (1-2 lines) with white space
- End with an engagement question
- CTA to follow at the end
- 150-250 words sweet spot
- No hashtags in body
"""

MASTER_PROMPT = """
You are a top LinkedIn content creator and AI analyst.
Task:
- Write a professional and engaging LinkedIn post about: {topic_label}
- Use the provided research brief for specific details.
- Focus on the latest trends and insights.

Structure:
- Hook (1 line): Provocative question, bold stat, or surprising fact.
- Insights: 3 short paragraphs (1-2 lines each) with white space.
- Engagement: One thought-provoking question at the end.
- CTA: Include the following CTA: "{follow_cta}"

Return ONLY valid JSON with:
{{
  "topic": "one-line topic",
  "hook": "the hook line",
  "point1": "first key insight",
  "point2": "second key insight",
  "point3": "third key insight",
  "takeaway": "the final takeaway/question",
  "image_prompt": "detailed prompt for a matching visual",
  "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}
"""
