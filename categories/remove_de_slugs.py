import json
import os

# read in the input file
input_file_path = os.path.join(os.path.dirname(__file__), 'slugs.json')
with open(input_file_path, 'r') as input_file:
    data = json.load(input_file)

#total number of books
total_books = 0

# create a set to keep track of all slugs
all_slugs = set()

# loop through each category and remove any book slugs that end with "-de"
for category in data['categories']:
    unique_slugs = []
    for slug in category['book_slugs']:
        # check if slug ends with "-de"
        if slug.endswith('-de'):
            continue
        # check if slug is already in the set
        if slug in all_slugs:
            continue
        # remove any text after "-en"
        if '-en' in slug:
            slug = '-en'.join(slug.split('-en')[:-1]) + '-en'
        unique_slugs.append(slug)
        all_slugs.add(slug)
    category['book_slugs'] = unique_slugs
    total_books += len(unique_slugs)
    print(f'Category {category["title"]} has {len(unique_slugs)} books')

print(f'Total books: {total_books}')

# write the updated data to a new file updated_slugs.json
output_file_path = os.path.join(os.path.dirname(__file__), 'updated_slugs.json')
with open(output_file_path, 'w') as output_file:
    json.dump(data, output_file, indent=4)

print('Done')
