#!/home/trezendes/.pyenv/versions/3.13.0/envs/CapBot/bin/python

from datetime import datetime
import json
from random import randint
from time import sleep
from typing import Any, BinaryIO, Optional, TextIO, TypedDict
from zoneinfo import ZoneInfo

from mastodon import AttribAccessDict, Mastodon


config_path: str = 'config.json'
config_file: TextIO
with open(config_path) as config_file:
    config: dict[str, str] = json.load(config_file)

secret: str = config['CLIENT_SECRET']
token: str = config['ACESS_TOKEN']
base_url: str = config['BASE_URL']

class MediaPathInnerDict(TypedDict):
    image: str
    description: str
    media_dict: Optional[AttribAccessDict]


cap_client: Mastodon = Mastodon(client_secret=secret, access_token=token, api_base_url=base_url,)

media_path_dict: dict[str, dict] = {
    'Page35': {
        'image': 'WI4435.jpg',
        'description': '35.txt'
    },
    'Page36': {
        'image': 'WI4436.jpg',
        'description': '36.txt'
    },
    'Page37': {
        'image': 'WI4437.jpg',
        'description': '37.txt'
    }
}

post_body: str = ''
hashtags: str = '#CaptainAmerica #WhatIf'
tz =  ZoneInfo('America/New_York')
post_windows = [(8, 12), (13, 17), (18, 22)]




def media_uploader(media_path: str, alt_file_path: str) -> AttribAccessDict:
    alt_file: TextIO
    media_file: BinaryIO
    with open(alt_file_path) as alt_file:
        alt_text: str = alt_file.read()
    with open(media_path, 'rb') as media_file:
        media_dict = cap_client.media_post(media_file, mime_type='image/jpeg', description=alt_text)
    return media_dict

def poster(media_dict: AttribAccessDict, post_window: tuple[int,int]) -> AttribAccessDict:
    current_date = datetime.now().strftime('%Y-%m-%d')
    hour: int = randint(post_window[0], post_window[1])
    minute = randint(0, 59)
    second = randint(0, 59)
    time_to_post: datetime = datetime.strptime(f'{current_date} {hour}:{minute}:{second}', '%Y-%m-%d %H:%M:%S')
    time_to_post.replace(tzinfo=tz)
    full_text: str
    if len(post_body) > 0:
        full_text = f'{post_body}\n{hashtags}'
    else:
        full_text = hashtags
    scheduled_status: AttribAccessDict = cap_client.status_post(full_text, media_ids=media_dict, scheduled_at=time_to_post, visibility='public', language='en')
    print(scheduled_status)
    return scheduled_status

index: int
key: str
value: dict
item: tuple[str,Any]

for key, value in media_path_dict.items():
    media_path: str = value['image']
    alt_file_path: str = value['description']
    value['media_dict'] = media_uploader(media_path, alt_file_path)
    sleep(5)

scheduled_toots: list[AttribAccessDict] = []

for index, item in enumerate(media_path_dict.items()):
    key = item[0]
    value = item[1]
    scheduled_status: AttribAccessDict = poster(value['media_dict'], post_windows[index])
    scheduled_toots.append(scheduled_status)
    sleep(5)

cur_time:str = datetime.now().strftime('%c')

verification_status_text: str = f"""
CapBot.py ran on {cur_time[:10]} at {cur_time[10:]}.
Statuses scheduled at:
Page 35: {scheduled_toots[0]['scheduled_at'].astimezone(tz).strftime('%H:%M:%S')}
Page 36: {scheduled_toots[1]['scheduled_at'].astimezone(tz).strftime('%H:%M:%S')}
Page 37: {scheduled_toots[2]['scheduled_at'].astimezone(tz).strftime('%H:%M:%S')}

#Schedule
"""


verification_status: AttribAccessDict = cap_client.status_post(verification_status_text, visibility='direct', language='en')