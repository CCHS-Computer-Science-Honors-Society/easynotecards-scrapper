import requests
import os
from bs4 import BeautifulSoup
import json
import sys
import re
import argparse
from urllib.parse import urlparse, urljoin

def scrape_easynotecards_to_json(url, output_file='flashcards.json', unit='', chapter=''):
    """
    Scrapes flashcards from the given EasyNoteCards URL and saves them to a JSON file.

    :param url: The URL of the EasyNoteCards page to scrape.
    :param output_file: The filename for the output JSON. Defaults to 'flashcards.json'.
    :param unit: The unit name to associate with the flashcards.
    :param chapter: The chapter name to associate with the flashcards.
    """
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/90.0.4430.93 Safari/537.36")
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all flashcard elements
    flashcards = soup.find_all('div', class_='vs-card')

    if not flashcards:
        print("No flashcards found on the page.")
        sys.exit(1)

    print(f"Found {len(flashcards)} flashcards. Extracting data...")

    # Prepare data for JSON
    data = []
    for idx, card in enumerate(flashcards, start=1):
        # Extract the question part
        term_div = card.find('div', class_='term')
        if not term_div:
            print(f"Flashcard {idx}: 'term' div not found. Skipping. {chapter}")
            continue

        question_text_div = term_div.find('div', class_='term-text')
        if not question_text_div:
            print(f"Flashcard {idx}: 'term-text' div not found. Skipping.")
            continue

        question_paragraphs = question_text_div.find_all('p')
        full_text = ''
        for paragraph in question_paragraphs:
            for br in paragraph.find_all('br'):
                br.replace_with('\n')
            full_text += paragraph.get_text(separator='\n').strip() + '\n'
        full_text = full_text.strip()

        # Split into lines
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]

        front = ""
        options = []
        current_option = ""
        option_labels = ['A)', 'B)', 'C)', 'D)', 'E)']

        contains_image_reference = False

        for line in lines:
            if "SEE IMAGE FOR CHOICES" in line.upper():
                contains_image_reference = True
                break
            # Check if the line starts with an option label
            if any(line.startswith(label) for label in option_labels):
                if current_option:
                    options.append(current_option.strip())
                current_option = line
            else:
                if current_option:
                    current_option += " " + line
                else:
                    front += line + " "

        # Append the last option
        if current_option:
            options.append(current_option.strip())

        front = front.strip()

        if contains_image_reference:
            options = ["[See image for choices]"]

        # Extract images with class "ei" within the flashcard
        images = []
        image_elements = card.find_all('img', class_='ei')
        for img in image_elements:
            img_src = img.get('src')
            if img_src:
                # Handle relative URLs
                if img_src.startswith('//'):
                    img_src = 'https:' + img_src
                elif img_src.startswith('/'):
                    parsed_url = urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    img_src = urljoin(base_url, img_src)
                elif not img_src.startswith('http://') and not img_src.startswith('https://'):
                    parsed_url = urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    img_src = urljoin(base_url, img_src)
                images.append(img_src)

        # Extract the answer part
        def_div = card.find('div', class_='def')
        if not def_div:
            answer = "No answer found."
        else:
            answer_paragraph = def_div.find('p')
            if answer_paragraph:
                answer_text = answer_paragraph.get_text(strip=True)
                _, _, answer = answer_text.partition('Answer:')
                answer = answer.strip()
            else:
                answer = "No answer text found."

        # Append the flashcard to data
        data.append({
            'front': front,
            'options': options,
            'back': answer,
            'unit': unit,
            'chapter': chapter,
            'images': images
        })

    # Write data to JSON
    try:
        os.makedirs("./data", exist_ok=True)
        with open(f"./data/{output_file}", 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        print(f"Flashcards successfully saved to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")
        sys.exit(1)


def parse_arguments():
    """
    Parses command-line arguments.

    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Scrape flashcards from EasyNoteCards and save to JSON.')
    parser.add_argument('url', help='URL of the EasyNoteCards page to scrape.')
    parser.add_argument('--output', '-o', default='flashcards.json', help='Output JSON file name. Defaults to flashcards.json.')
    parser.add_argument('--unit', '-u', required=True, help='Unit name to associate with the flashcards.')
    parser.add_argument('--chapter', '-c', required=True, help='Chapter name to associate with the flashcards.')
    
    return parser.parse_args()

def do():
    indexToUrl = {
        1: 'https://www.easynotecards.com/notecard_set/89356',
    2: 'https://www.easynotecards.com/notecard_set/89357',
    3: 'https://www.easynotecards.com/notecard_set/89358',
    4: 'https://www.easynotecards.com/notecard_set/89359',
    5: 'https://www.easynotecards.com/notecard_set/89360',
    6: 'https://www.easynotecards.com/notecard_set/89361',
    7: 'https://www.easynotecards.com/notecard_set/89362',
    8: 'https://www.easynotecards.com/notecard_set/89363',
    9: 'https://www.easynotecards.com/notecard_set/87887',
    10: 'https://www.easynotecards.com/notecard_set/87898',
    11: 'https://www.easynotecards.com/notecard_set/89364',
    12: 'https://www.easynotecards.com/notecard_set/89365',
    13: 'https://www.easynotecards.com/notecard_set/89366',
    14: 'https://www.easynotecards.com/notecard_set/89367',
    15: 'https://www.easynotecards.com/notecard_set/89368',
    16: 'https://www.easynotecards.com/notecard_set/88917',
    17: 'https://www.easynotecards.com/notecard_set/88921',
    18: 'https://www.easynotecards.com/notecard_set/88919',
    19: 'https://www.easynotecards.com/notecard_set/88845',
    20: 'https://www.easynotecards.com/notecard_set/88846',
    21: 'https://www.easynotecards.com/notecard_set/88972',
    22: 'https://www.easynotecards.com/notecard_set/88916',
    23: 'https://www.easynotecards.com/notecard_set/88935',
    24: 'https://www.easynotecards.com/notecard_set/88936',
    25: 'https://www.easynotecards.com/notecard_set/89070',
    26: 'https://www.easynotecards.com/notecard_set/89072',
    27: 'https://www.easynotecards.com/notecard_set/88847',
    28: 'https://www.easynotecards.com/notecard_set/89068',
    29: 'https://www.easynotecards.com/notecard_set/89198',
    30: 'https://www.easynotecards.com/notecard_set/89302',
    31: 'https://www.easynotecards.com/notecard_set/89256',
    32: 'https://www.easynotecards.com/notecard_set/89201',
    33: 'https://www.easynotecards.com/notecard_set/89303',
    34: 'https://www.easynotecards.com/notecard_set/89146',
    35: 'https://www.easynotecards.com/notecard_set/88971',
    36: 'https://www.easynotecards.com/notecard_set/88970',
    37: 'https://www.easynotecards.com/notecard_set/88968',
    38: 'https://www.easynotecards.com/notecard_set/88967',
    39: 'https://www.easynotecards.com/notecard_set/88965',
    40: 'https://www.easynotecards.com/notecard_set/88751',
    41: 'https://www.easynotecards.com/notecard_set/89014',
    42: 'https://www.easynotecards.com/notecard_set/89013',
    43: 'https://www.easynotecards.com/notecard_set/88754',
    44: 'https://www.easynotecards.com/notecard_set/89371',
    45: 'https://www.easynotecards.com/notecard_set/89372',
    46: 'https://www.easynotecards.com/notecard_set/89372',
    47: 'https://www.easynotecards.com/notecard_set/89374',
    48: 'https://www.easynotecards.com/notecard_set/89375',
    49: 'https://www.easynotecards.com/notecard_set/89376',
    50: 'https://www.easynotecards.com/notecard_set/89377',
    51: 'https://www.easynotecards.com/notecard_set/89379',
    52: 'https://www.easynotecards.com/notecard_set/89380',
    53: 'https://www.easynotecards.com/notecard_set/89381',
    54: 'https://www.easynotecards.com/notecard_set/89382',
    55: 'https://www.easynotecards.com/notecard_set/89370'
    }
    
    for i in range(1, 56):
        url = indexToUrl[i]
        output_file = f"flashcards_{i}.json"
        unit = f"Unit {i}"
        chapter = f"Chapter {i}"
        scrape_easynotecards_to_json(url, output_file, unit, chapter)



if __name__ == "__main__":
    do()
