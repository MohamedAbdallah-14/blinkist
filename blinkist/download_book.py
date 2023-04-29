#!/usr/bin/env python3
from pathlib import Path

from blinkist.book import Book  # typing only
from blinkist.console import console, status, track


def download_book(
    book: Book,
    language: str,
    library_dir: Path,
    # ---
    yaml: bool = True,
    markdown: bool = True,
    audio: bool = True,
    cover: bool = True,
    # ---
    redownload: bool = False,
    continue_on_error: bool = False,
    # ---
    **kwargs,
):
    # check library directory
    # This comes first so we can fail early if the path doesn't exist.
    assert library_dir.exists()

    # setup book directory
    # book_dir = library_dir / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir = library_dir / book.slug
    if book_dir.exists() and not redownload:
        console.print(f"Skipping „{book.title}“ – already downloaded.")
        # TODO: this doss not check if the download was complete! Can we do something about that
        return
    # We don't make parents in order to avoid user error.
    book_dir.mkdir(exist_ok=True)

    try:
        # prefetch chapter_list and chapters for nicer progress info
        with status("Retrieving list of chapters for book " + book.slug + "…"):
            _ = book.chapter_list
        # this displays a progress bar itself ↓
        _ = book.chapters

        # download raw (YAML)
        # This comes first so we have all information saved as early as possible.
        if yaml:
            with status("Downloading raw YAML " + book.slug + "…"):
                book.download_raw_yaml(book_dir)

        # download text (Markdown)
        if markdown:
            with status("Downloading text " + book.slug + "…"):
                book.download_text_md(book_dir)

        # download audio
        if audio:
            if book.is_audio:
                for chapter in track(book.chapters, description="Downloading audio " + book.slug + "…"):
                    chapter.download_audio(book_dir)
            else:
                console.print("This book has no audio.")

        # download cover
        if cover:
            with status("Downloading cover " + book.slug + "…"):
                book.download_cover(book_dir)
    except Exception as e:
        console.print(f"Error downloading „{book.title}“: {e}")

        error_dir = book_dir.parent / f"{book.slug} – ERROR"
        i = 0
        while error_dir.exists() and any(error_dir.iterdir()):
            i += 1
            error_dir = book_dir.parent / f"{book.slug} – ERROR ({i})"

        console.print(
            f"Renaming output directory to “{error_dir.relative_to(book_dir.parent)}”")
        book_dir.replace(target=error_dir)

        if continue_on_error:
            console.print(
                "Continuing with next book… (--continue-on-error was set)")
        else:
            console.print(
                "Exiting…", "Hint: Try using --continue-on-error.", sep="\n")
            raise
