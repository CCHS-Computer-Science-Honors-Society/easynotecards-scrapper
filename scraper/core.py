import sys
from .fetch import fetch_page
from .parse import parse_flashcards
from .extract import extract_flashcard_data
from .save import save_to_json, save_to_csv

def scrape_easynotecards(url, unit='', chapter=''):
    """
    Scrapes flashcards from the given EasyNoteCards URL.

    :param url: The URL of the EasyNoteCards page to scrape.
    :param unit: The unit name to associate with the flashcards.
    :param chapter: The chapter name to associate with the flashcards.
    :return: A list of dictionaries containing flashcard data.
    """
    html = fetch_page(url)
    flashcard_elements = parse_flashcards(html)

    if not flashcard_elements:
        raise ValueError("No flashcards found on the page.")

    print(f"Found {len(flashcard_elements)} flashcards. Extracting data...")

    data = []
    for idx, card in enumerate(flashcard_elements, start=1):
        try:
            flashcard = extract_flashcard_data(card, url)
            flashcard['unit'] = unit
            flashcard['chapter'] = chapter
            data.append(flashcard)
        except ValueError as ve:
            print(f"Flashcard {idx}: {ve} Skipping.")
            continue

    return data

def scrape_and_save(url, output_file='data/flashcards.json', unit='', chapter='', format='json'):
    """
    Scrapes flashcards from the given EasyNoteCards URL and saves them to a file.

    :param url: The URL of the EasyNoteCards page to scrape.
    :param output_file: The filename for the output file.
    :param unit: The unit name to associate with the flashcards.
    :param chapter: The chapter name to associate with the flashcards.
    :param format: The format to save the data ('json' or 'csv').
    """
    try:
        data = scrape_easynotecards(url, unit, chapter)
        if format.lower() == 'json':
            save_to_json(data, output_file)
            print(f"Flashcards successfully saved to '{output_file}'.")
        elif format.lower() == 'csv':
            save_to_csv(data, output_file)
            print(f"Flashcards successfully saved to '{output_file}'.")
        else:
            print(f"Unsupported format: {format}. Please choose 'json' or 'csv'.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except IOError as ioe:
        print(f"Error writing to file: {ioe}")
        sys.exit(1)
