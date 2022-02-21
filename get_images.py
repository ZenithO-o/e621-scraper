import json
import requests
from io import BytesIO
from PIL import Image

ML_SIZE   = (512,512)
DATA_FILE = 'data/posts.json'

def load_posts() -> dict:
    try:
        with open(DATA_FILE, encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def create_image(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to collect image. ({response.status_code})')
        return None
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img1 = img.resize(ML_SIZE)
    return img1

posts = load_posts()

for item in list(posts.items()):
    url = item[1]['url']
    ext = url[url.rfind("."):]
    print(f'creating image {item[0]}.png')
    print(url)
    image = create_image(item[1]['url'])
    if image:
        image.save(f'images/{item[0]}.png')