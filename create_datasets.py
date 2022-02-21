import json
import os 

DATA_FILE = 'data/posts.json'
TAG_FILE  = 'data/tags_list.json'

def load_posts_saved() -> list:
    posts = os.listdir('images/')
    posts = [p[:p.rfind('.')] for p in posts]
    return posts

def load_posts_dict() -> dict:
    try:
        with open(DATA_FILE, encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def load_tags() -> dict:
    with open(TAG_FILE, encoding='utf-8') as json_file:
        tags = json.load(json_file)
        tags['species'] = list(tags['species'])
        tags['general'] = list(tags['general'])
        return tags

def create_onehot(length, positions):
    l = [0] * length
    for pos in positions:
        l[pos] = 1
    return l

tags = load_tags()
species_len = len(tags['species'])
general_len = len(tags['general'])

posts = load_posts_saved()
post_dict = load_posts_dict()

s_header = f"id, {', '.join(tags['species'])}\n"
g_header = f"id, {', '.join(tags['general'])}\n"

s_lines = [s_header]
g_lines = [g_header]

for post in posts:
    species_intersect = set(post_dict[post]['species']).intersection(tags['species'])
    s_positions = [tags['species'].index(s) for s in species_intersect]
    s_onehot = create_onehot(species_len, s_positions)

    general_intersect = set(post_dict[post]['general']).intersection(tags['general'])
    g_positions = [tags['general'].index(g) for g in general_intersect]
    g_onehot = create_onehot(general_len, g_positions)
    
    s_line = f"{post}, {', '.join(map(str, s_onehot))}\n"
    s_lines.append(s_line)

    g_line = f"{post}, {', '.join(map(str, g_onehot))}\n"
    g_lines.append(g_line)


with open('data/species_dataset.csv', 'w', encoding='utf-8') as csv_file:
    csv_file.writelines(s_lines)


with open('data/general_dataset.csv', 'w', encoding='utf-8') as csv_file:
    csv_file.writelines(g_lines)
