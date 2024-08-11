import json
import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

COMMON_HEADERS = {
    "Content-Type": "text/plain;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://suno.com",
    "Origin": "https://suno.com",
}


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)

    print(data, method, headers, url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method, url=url, data=data, headers=headers
            ) as resp:
                return await resp.json()
        except Exception as e:
            return f"An error occurred: {e}"


async def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/?ids={ids}"
    response = await fetch(api_url, headers, method="GET")
    return response


async def generate_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/v2/"
    response = await fetch(api_url, headers, data)
    return response


async def generate_lyrics(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/"
    data = {"prompt": prompt}
    return await fetch(api_url, headers, data)


async def get_lyrics(lid, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/{lid}"
    return await fetch(api_url, headers, method="GET")


async def get_credits(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/billing/info/"
    response = await fetch(api_url, headers, method="GET")
    return {
        "credits_left": response["total_credits_left"],
        "period": response["period"],
        "monthly_limit": response["monthly_limit"],
        "monthly_usage": response["monthly_usage"],
    }


async def get_upload_audio_s3_link(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/uploads/audio/"
    response = await fetch(api_url, headers, method="GET")
    return {
        "url": response["url"],
        "id": response["id"],
        "fields": response["fields"],
    }


async def upload_audio(token, file, url: str, fields: dict):
    # 파일을 열고, Content-Type과 키를 지정하여 헤더 및 폼 데이터를 설정합니다.
    headers = {"Authorization": f"Bearer {token}"}

    # 비동기 HTTP 요청을 통해 파일을 전송합니다.
    async with aiohttp.ClientSession() as session:
        with open(file, "rb") as f:
            files = {"file": ("audio/mpeg", f, "audio/mpeg")}

            async with session.post(
                url, headers=headers, data=fields, files=files
            ) as response:
                if response.status == 200:
                    print("File uploaded successfully")
                else:
                    print(f"Failed to upload file. Status code: {response.status}")
            return response


async def upload_audio_to_clip(token, file_id: str):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/uploads/audio/{file_id}/initialize-clip/"
    response = await fetch(api_url, headers, method="POST")
    return {
        "clip_id": response["clip_id"],
    }
