import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    # print(f'Categories Progress: {current}/{total} ({progress:.2f}%)')

# define the books progress indicator function
def print_books_progress(current, total):
    progress = current / total * 100
    # print(f'Books Progress: {current}/{total} ({progress:.2f}%)')

# define the function to get book data
def get_book_data(book_id):
    try:
        response = requests.get(f'https://api.blinkist.com/v4/books/{book_id}')
        if response.status_code == 200:
            book_data = response.json()
            book_slug = book_data['book']['slug']
            return book_slug
        else:
            # print(f'Error: Failed to get book data for book ID {book_id}. Response code: {response.status_code}')
            return None
    except Exception as e:
        # print(f'Error: Failed to get book data for book ID {book_id}. Exception: {e}')
        return None

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
        print(f'Warning: Category {category_name} does not have an "en" i18n')

    # create the folder for the category
    folder_path = os.path.join(output_folder_path, category_name)
    os.makedirs(folder_path, exist_ok=True)

    # print(f'Getting books for category {category_name}...')

    # get the book slugs for the category
    book_slugs = []
    book_ids = category['book_ids']
    total_books = len(book_ids)
    # with ThreadPoolExecutor(max_workers=50) as executor:
    #     futures = [executor.submit(get_book_data, book_id) for book_id in book_ids]
    #     for future in as_completed(futures):
    #         book_slug = future.result()
    #         if book_slug:
    #             book_slugs.append(book_slug)
            
            # print book progress
            # print_books_progress(len(book_slugs), total_books)

    # add the category data to the output data
    category_data = {
        'id': category['id'],
        'title': category_name,
        'dir_path': folder_path,
        'book_slugs': book_slugs
    }
    output_data['categories'].append(category_data)

    # write the output data to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

    # print the progress
    # print_progress(i, len(input_data['categories']))

# print('Done')
