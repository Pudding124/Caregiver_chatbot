import json

class CaresInfo:
    def __init__(self, id, name, description, language, locations, service_rule):
        self.id = id
        self.name = name
        self.description = description
        self.language = language
        self.locations = locations
        self.service_rule = service_rule
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "language": self.language,
            "locations": self.locations,
            "service_rule": self.service_rule
        }


# Replace 'filename.json' with the path to your JSON file
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


personal_info = data['form']['searchListings']['results']


all_cares = []
for content in personal_info:
    id = content['meta']['id']
    name = content['content']['userProfiles']['nurse']['name']['lastName'] + content['content']['userProfiles']['nurse']['name']['firstName']
    description = content['content']['description']['value']
    languages = [lang for lang, value in content['content']['languages'].items() if value]
    location = cities = [pair['city'] for pair in content['content']['locations']['pairs']]
    service_rule = []
    for category, items in content['content']['services'].items():
        for service, is_true in items.items():
            if is_true:
                service_rule.append(service)
    
    care = CaresInfo(id, name, description, languages, location, service_rule)
    all_cares.append(care.to_dict())


print(all_cares)


# Write data to a JSON file
with open('tide_up_data.json', 'w', encoding='utf-8') as file:
    json.dump(all_cares, file, ensure_ascii=False, indent=4)

