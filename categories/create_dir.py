import json
import os
import requests

# read the input json file
input_file_path = os.path.join(os.path.dirname(__file__), 'categories.json')
with open(input_file_path, 'r') as input_file:
    input_data = json.load(input_file)

# define the output folder path and json file name
output_folder_path = os.path.join(os.path.dirname(__file__), 'Download', 'Categories')
output_file_path = os.path.join(os.path.dirname(__file__), 'output.json')

# define the progress indicator function
def print_progress(current, total):
    progress = current / total * 100
    print(f'Categories Progress: {current}/{total} ({progress:.2f}%)')

# define the books progress indicator function
def print_books_progress(current, total):
    progress = current / total * 100
    print(f'Books Progress: {current}/{total} ({progress:.2f}%)')

# initialize the output data
output_data = {'categories': []}

# loop through each category and create a folder for it
for i, category in enumerate(input_data['categories'], start=1):
    # get the category name in the "en" language
    en_i18n = next((i18n for i18n in category['i18ns'] if i18n['language'] == 'en'), None)
    if en_i18n:
        category_name = en_i18n['title']
    else:
        category_name = category['id']

    # create the folder for the category
    folder_path = os.path.join(output_folder_path, category_name)
    os.makedirs(folder_path, exist_ok=True)

    print(f'Getting books for category {category_name}...')

    # get the book slugs for the category
    book_slugs = []
    for book_id in category['book_ids']:
        #print book progress
        print_books_progress(len(book_slugs), len(category['book_ids']))
        # make the API call to get the book data
        response = requests.get(f'https://api.blinkist.com/v4/books/{book_id}')
        if response.status_code == 200:
            book_data = response.json()
            book_slug = book_data['book']['slug']
            book_slugs.append(book_slug)
        else:
            print(f'Error: Failed to get book data for book ID {book_id}. Response code: {response.status_code}')

    # add the category data to the output data
    category_data = {
        'id': category['id'],
        'title': category_name,
        'dir_path': folder_path,
        'book_slugs': book_slugs
    }
    output_data['categories'].append(category_data)

    # print the progress
    print_progress(i, len(input_data['categories']))

# save the output data to the output json file
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=2)

print('Done')
