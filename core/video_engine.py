# core/video_engine.py
import os
import requests
import random
from moviepy import ImageClip  # Inayos para sa MoviePy v2 standard layout
from shared.settings import settings

def scrape_anime_horror_image(keyword: str) -> str:
    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("[VIDEO ENGINE]: Missing Pexels API Key Node.")
        return ""
    
    anime_keyword = f"dark anime {keyword} illustration graphic"
    url = f"https://pexels.com{anime_keyword}&per_page=8"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=12)
        data = response.json()
        if data.get("photos"):
            photo = random.choice(data["photos"])
            return photo["src"]["large2x"]
    except Exception as e:
        print(f"[SCRAPER EXCEPTION]: {e}")
    return ""

def render_standalone_video(keyword: str, duration: float, output_path: str):
    img_temp = output_path + ".temp.jpg"
    image_url = scrape_anime_horror_image(keyword)
    
    try:
        if image_url:
            img_data = requests.get(image_url).content
            with open(img_temp, "wb") as f:
                f.write(img_data)
                
            video_clip = ImageClip(img_temp).set_duration(duration)
            video_clip = video_clip.resize(lambda t: 1 + 0.12 * (t / duration))
            
            video_clip.write_videofile(
                output_path, 
                fps=24, 
                codec="libx264", 
                audio=False,
                verbose=False,
                logger=None
            )
            video_clip.close()
            return True
        return False
    except Exception as e:
        print(f"[VIDEO COMPILING CRASH]: {e}")
        raise e
    finally:
        if os.path.exists(img_temp):
            os.remove(img_temp)
