import json
import requests
import datetime
from config.config import GROQ_API_KEY, MASTER_PROMPT, LINKEDIN_BEST_PRACTICES

def generate_content(research_brief: str, topic_config: dict) -> dict:
    print(f"✍️  Generating AI summary for: {topic_config['name']}...")
    
    today = datetime.date.today().strftime("%B %d, %Y")
    
    system_prompt = MASTER_PROMPT.format(
        topic_label=topic_config['label'],
        follow_cta=topic_config['follow_cta']
    )
    
    # Add LinkedIn Best Practices to the prompt
    system_prompt += f"\n\nContext on LinkedIn Performance:\n{LINKEDIN_BEST_PRACTICES}"

    user_message = f"Today is {today}. Context: {topic_config['label']}\n\n{research_brief}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    
    data = response.json()["choices"][0]["message"]["content"]
    return json.loads(data)
