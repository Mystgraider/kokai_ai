import os
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from shared.settings import settings

def upload_to_youtube(video_path: str, title: str, description: str):
    if not settings.YOUTUBE_CLIENT_SECRETS:
        print("[YOUTUBE WARNING]: Missing client configuration secrets payload.")
        return "UPLOAD_SKIPPED"
        
    with open("temp_secrets.json", "w") as f:
        f.write(settings.YOUTUBE_CLIENT_SECRETS)

    scopes = ["https://googleapis.com"]
    flow = InstalledAppFlow.from_client_secrets_file("temp_secrets.json", scopes)
    credentials = flow.run_local_server(port=0)
    
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["aswang", "horror", "tagalog", "kokai_ai"],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "public"
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    
    if os.path.exists("temp_secrets.json"):
        os.remove("temp_secrets.json")
        
    return f"https://youtube.com{response.get('id')}"

def upload_to_facebook(video_path: str, title: str, description: str):
    if not settings.FACEBOOK_PAGE_ID or not settings.FACEBOOK_ACCESS_TOKEN:
        print("[FACEBOOK WARNING]: Missing active page ID or authentication tokens.")
        return {"status": "SKIPPED"}
        
    url = f"https://facebook.com{settings.FACEBOOK_PAGE_ID}/videos"
    payload = {
        "title": title,
        "description": description,
        "access_token": settings.FACEBOOK_ACCESS_TOKEN
    }
    
    with open(video_path, "rb") as video_file:
        files = {"source": video_file}
        response = requests.post(url, data=payload, files=files)
        
    return response.json()
