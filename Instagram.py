import os
from instagrapi import Client
import aiohttp
import aiofiles

async def download_file(url: str, filename: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            async with aiofiles.open(filename, 'wb') as f:
                await f.write(content)
    return filename

async def post_to_instagram(url: str, caption: str) -> None:
    cl = Client()
    cl.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))

    filename = await download_file(url, 'temp.jpg')
    cl.photo_upload(filename, caption)
    os.remove(filename)