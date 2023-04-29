from pathlib import Path

import json
import os
import datetime

from blinkist.book import Book  # typing only
from blinkist.download_book import download_book
from blinkist.console import console, track, track_context


# read the input json file
input_file_path = os.path.join(os.path.dirname(__file__), 'updated_slugs.json')
with open(input_file_path, 'r') as input_file:
    input_data = json.load(input_file)

# define the output folder path and json file name
output_folder_path = os.path.join(os.path.dirname(__file__), 'Download', 'Categories')
output_file_path = os.path.join(os.path.dirname(__file__), 'output.json')

# define the progress indicator function

def print_progress(current, total):
    progress = current / total * 100
    console.print(f'Categories Progress: {current}/{total} ({progress:.2f}%)')

# define the books progress indicator function


def print_books_progress(current, total):
    progress = current / total * 100
    console.print(f'Books Progress: {current}/{total} ({progress:.2f}%)')


# initialize the output data
output_data = {'categories': []}

# loop through each category and create a folder for it
for i, category in enumerate(input_data['categories'], start=1):
    category_name = category['title']

    # create the folder for the category
    folder_path = os.path.join(output_folder_path, category_name)
    os.makedirs(folder_path, exist_ok=True)

    console.print(f'Getting books for category {category_name}...')

    # get the book slugs for the category
    book_names = []
    # books_progress = 0
    book_slugs = category['book_slugs']
    with track_context:
        for book_slug in (
            track(
                book_slugs, description="Downloading books for category " + category_name + "…")
            if len(book_slugs) > 1
            else book_slugs
        ):
            # print book progress
            # books_progress += 1
            # print_books_progress(books_progress, len(category['book_slugs']))
            # if book_slug directory exists, skip
            if os.path.exists(os.path.join(folder_path, book_slug)):
                console.print(f"Skipping {book_slug} – already downloaded.")
                continue

            # make the API call to get the book data
            try:
                book = Book.from_slug(book_slug)
                if book:
                    book_name = book.title
                    book_names.append(book_name)
                else:
                    console.print(
                        f'Error: Failed to get book data for book slug {book_slug}')

                download_book(book=book, language='en',
                              library_dir=Path(folder_path))
            except Exception as e:
                console.print(
                    f'Error: Failed to get book data for book slug {book_slug}')
                console.print(e)
                continue

    # add the category data to the output data
    category_data = {
        'id': category['id'],
        'title': category_name,
        'dir_path': folder_path,
        'book_names': book_names
    }
    output_data['categories'].append(category_data)

    # write the output data to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

    # print category progress
    print_progress(i, len(input_data['categories']))

console.print('Done!')
