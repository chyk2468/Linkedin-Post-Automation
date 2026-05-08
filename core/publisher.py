import requests
from typing import Optional
from config.config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN

def upload_image_to_linkedin(image_path: str) -> Optional[str]:
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    register_payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": LINKEDIN_PERSON_URN,
            "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
        }
    }
    r = requests.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers=headers,
        json=register_payload
    )
    r.raise_for_status()
    resp_data = r.json()
    upload_url = resp_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_urn = resp_data["value"]["asset"]

    with open(image_path, "rb") as f:
        requests.put(
            upload_url,
            headers={
                "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
                "Content-Type": "application/octet-stream"
            },
            data=f.read()
        )
    return asset_urn

def post_to_linkedin(post_text: str, image_path: Optional[str] = None) -> str:
    print("🚀 Publishing to LinkedIn...")
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": LINKEDIN_PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    
    if image_path:
        try:
            asset_urn = upload_image_to_linkedin(image_path)
            if asset_urn:
                payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{
                    "status": "READY",
                    "media": asset_urn,
                    "title": {"text": "AI Daily Insights"}
                }]
        except Exception as e:
            print(f"   [WARN] Image upload failed, posting text only: {e}")

    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=payload
    )
    r.raise_for_status()
    post_id = r.headers.get("x-restli-id")
    print(f"   ✅ Posted! ID: {post_id}")
    return post_id
