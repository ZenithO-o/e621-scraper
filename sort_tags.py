import json

with open('data/general_tags.json') as json_file:
    general = list(json.load(json_file)["tags"])

with open('data/species_tags.json') as json_file:
    species = list(json.load(json_file)["tags"])

CUTOFF = 7000

species.sort(key= lambda x: x['post_count'], reverse=True)
species = [s for s in species if s['post_count'] > CUTOFF]
general.sort(key= lambda x: x['post_count'], reverse=True)
general = [g for g in general if g['post_count'] > CUTOFF]

tags = {"species": [s['name'] for s in species], "general": [g['name'] for g in general]}

with open('data/tags_list.json', 'w', encoding='utf-8') as json_file:
    json.dump(tags, json_file, indent=2, ensure_ascii=False)