import urllib.request
import json
import os
import re

video_id = "7678374041442422036"
video_url = "https://www.tiktok.com/@leo.nail.zone/video/" + video_id
output_thumb = os.path.join("assets", "thumbnails", f"thumb_{video_id}.jpg")
os.makedirs(os.path.join("assets", "thumbnails"), exist_ok=True)

# Free public TikTok API endpoints that don't rate limit or require cookies
endpoints = [
    f"https://api.tiklydown.eu.org/api/download?url=https://www.tiktok.com/@leo.nail.zone/video/{video_id}",
    f"https://www.tikwm.com/api/?url=https://www.tiktok.com/@leo.nail.zone/video/{video_id}",
    f"https://api.douyin.wtf/tiktok?url=https://www.tiktok.com/@leo.nail.zone/video/{video_id}"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

downloaded = False

for ep in endpoints:
    try:
        print(f"Trying endpoint: {ep.split('/')[2]}...")
        req = urllib.request.Request(ep, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
            # Extract cover URL from various API responses
            cover_url = None
            if "data" in data and isinstance(data["data"], dict):
                cover_url = data["data"].get("cover") or data["data"].get("origin_cover") or data["data"].get("dynamic_cover")
            elif "cover" in data:
                cover_url = data.get("cover")
            elif "video" in data and isinstance(data["video"], dict):
                cover_url = data["video"].get("cover")
                
            if cover_url:
                print(f"Found cover: {cover_url[:60]}...")
                img_req = urllib.request.Request(cover_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp, open(output_thumb, "wb") as f:
                    f.write(img_resp.read())
                print(f"\n>>> [SUCCESS] Saved thumbnail to: {output_thumb} <<<")
                downloaded = True
                break
    except Exception as e:
        print(f"Endpoint failed: {e}")

if not downloaded:
    print("Could not download automatically. Please check your internet connection.")
