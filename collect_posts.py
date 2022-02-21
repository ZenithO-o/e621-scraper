from monosodium_glutamate import E621Wrapper
import json

DATA_FILE = 'data/posts.json'

def convert_rating(rating: str) -> list:
    if rating == 's':
        return [1, 0, 0]
    if rating == 'e':
        return [0, 1, 0]
    return [0, 0, 1]

def load_posts() -> dict:
    try:
        with open(DATA_FILE, encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def save_posts(posts: dict) -> None:
    print(f'saving {len(posts)} posts')
    with open(DATA_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(posts, json_file, indent=2,ensure_ascii=False)

def get_last_post() -> str:
    try:
        with open(DATA_FILE, encoding='utf-8') as json_file:
            posts = json.load(json_file)
            keys = posts.keys()
            return 'b' + str(list(keys)[-1])
    except FileNotFoundError:
        return None

with open('key.json') as json_file:
    key = json.load(json_file)["key"]

e = E621Wrapper('zenithO_o', key, 'TagScraper zenithO_o')

tags = ["-animated", "-webm", "-flash", "-3d_(artwork)", "-sketch", "-pixel_(artwork)", "~digital_media_(artwork)", "~traditional_media_(artwork)"]
print(' '.join(tags))
print(get_last_post())
last_post = get_last_post()
all_posts = load_posts()
save_count = 0
while len(all_posts) < 3200:
    posts = e.get_posts(limit=320, tags=tags, page=last_post)
    if len(posts) == 0:
        break
    
    last_post = 'b' + str(posts[-1]["id"])
    print(last_post)

    for post in posts:
        post_id = post['id']
        url = post['file']['url']
        ext = post['file']['ext']
        rating = post['rating']
        species = post['tags']['species']
        general = post['tags']['general']
        score = post['score']['total']
        if ext in ['png', 'jpg']:
            all_posts[str(post_id)] = {
                "url"     : url,
                "rating"  : convert_rating(rating),
                "score"   : score,
                "species" : species,
                "general" : general
                }
        
    save_count += 1
    if save_count % 10 == 0:
        save_posts(all_posts)

save_posts(all_posts)
