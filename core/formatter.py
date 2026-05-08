def format_post(data: dict, topic_config: dict) -> str:
    """Standardizes the raw LLM output into a clean LinkedIn post."""
    
    # Use emojis for better engagement
    post = f"🚀 {data['hook']}\n\n"
    
    post += f"🔹 {data['point1']}\n\n"
    post += f"🔹 {data['point2']}\n\n"
    post += f"🔹 {data['point3']}\n\n"
    
    post += f"💡 {data['takeaway']}\n\n"
    
    post += f"{topic_config['follow_cta']}\n\n"
    
    # Append hashtags
    hashtags = data.get('hashtags', topic_config['hashtags'])
    post += " ".join(f"#{h.replace('#', '')}" for h in hashtags)
    
    return post
