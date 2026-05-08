import requests
import datetime
from pathlib import Path
from config.config import OUTPUT_DIR, PEXELS_API_KEY

def generate_image(image_prompt: str, topic: str):
    """
    Sourcing images from Pexels API instead of generating them.
    Returns: (image_path, attribution_text)
    """
    if not PEXELS_API_KEY:
        print("   [WARN] PEXELS_API_KEY not found in config. Skipping image sourcing.")
        return "", ""

    print(f"🔍 Searching Pexels for: {topic[:30]}...")
    
    headers = {"Authorization": PEXELS_API_KEY}
    
    # Clean up the prompt for search - AI prompts are often too long for stock search
    search_query = image_prompt[:100] if len(image_prompt) > 20 else topic
    
    try:
        url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1&orientation=landscape"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("photos"):
            # Fallback to topic if specific prompt failed
            print(f"   [INFO] No results for '{search_query}', trying topic fallback...")
            url = f"https://api.pexels.com/v1/search?query={topic}&per_page=1&orientation=landscape"
            response = requests.get(url, headers=headers, timeout=30)
            data = response.json()
            
        if data.get("photos"):
            photo = data["photos"][0]
            image_url = photo["src"]["large"] 
            photographer = photo.get("photographer", "Unknown")
            photographer_url = photo.get("photographer_url", "https://www.pexels.com")
            
            attribution = f"Photo by {photographer} on Pexels"
            
            print(f"   [INFO] Found image by {photographer}. Downloading...")
            
            # Download the image
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            date_str = datetime.date.today().strftime("%Y%m%d")
            safe_topic = "".join(c if c.isalnum() else "_" for c in topic)[:40]
            image_path = OUTPUT_DIR / f"pexels_{date_str}_{safe_topic}.jpg"
            
            with open(image_path, "wb") as f:
                f.write(img_response.content)
                
            print(f"   ✅ Image saved: {image_path.name}")
            return str(image_path), attribution
        else:
            print(f"   [WARN] No images found on Pexels for '{topic}'.")
            return "", ""
            
    except Exception as e:
        print(f"   [WARN] Pexels image sourcing failed: {e}")
        return "", ""
