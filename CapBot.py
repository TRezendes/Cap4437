import json
from typing import BytesIO, TextIO, TypedDict

from mastodon import Mastodon

config_path: str = 'config.json'
config_file: TextIO
with open(config_path) as config_file:
    config: dict[str, str] = json.load(config_file)

key: str = config['CLIENT_KEY']
secret: str = config['CLIENT_SECRET']
token: str = config['ACESS_TOKEN']
base_url: str = config['BASE_URL']

class MetaSizeDict(TypedDict):
    width: int
    height: int
    size: str
    aspect: float

class MediaDict(TypedDict):
    id : int
    type: str
    url: str
    preview_url: str
    remote_url: str | None
    preview_remote_url: str | None
    text_url: str | None
    meta: dict[str, dict[str, MetaSizeDict]]
    description: str
    blurhash: str

class MediaPathInnerDict(TypedDict):
    image: str
    description: str
    media_dict: MediaDict | None

cap_client: Mastodon = Mastodon(client_secret=secret, access_token=token, api_base_url=None,)
def media_uploader(media_path: str, alt_file_path: str) -> MediaDict:
    alt_file: TextIO
    media_file: BytesIO
    with open(alt_file_path) as alt_file:
        alt_text: str = alt_file.read()
    with open(media_path, 'rb') as media_file:
        media_dict = cap_client.media_post(media_file, mime_type='image/jpeg', description=alt_text)
    return media_dict

media_path_dict: dict[str, MediaPathInnerDict] = {
    'Page35': {
        'image': 'WI4435.jpg',
        'description': '35.txt',
        'media_dict': None
    },
    'Page36': {
        'image': 'WI4436.jpg',
        'description': '36.txt',
        'media_dict': None
    },
    'Page37': {
        'image': 'WI4437.jpg',
        'description': '37.txt',
        'media_dict': None
    }
}

for key, value in media_path_dict.items():
    media_path: str = value['image']
    alt_file_path: str = value['description']
    media_path_dict[key]['media_dict'] = media_uploader(media_path, alt_file_path)