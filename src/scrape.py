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
            print(f"Flashcard {idx}: 'term' div not found. Skipping.")
            continue  # Skip if term div is not found

        question_text_div = term_div.find('div', class_='term-text')
        if not question_text_div:
            print(f"Flashcard {idx}: 'term-text' div not found. Skipping.")
            continue  # Skip if question text div is not found

        # Extract text and split by <br> tags
        question_paragraph = question_text_div.find('p')
        if question_paragraph:
            # Replace <br> tags with newline characters
            for br in question_paragraph.find_all('br'):
                br.replace_with('\n')
            # Get the full text with newlines
            full_text = question_paragraph.get_text(separator='\n').strip()
            # Split into lines
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            if not lines:
                front = "No question text found."
                options = []
            else:
                # Initialize front and options
                front = ""
                options = []
                current_option = ""
                option_labels = ['A)', 'B)', 'C)', 'D)', 'E)']

                for line in lines:
                    # Check if the line starts with an option label
                    if any(line.startswith(label) for label in option_labels):
                        if current_option:
                            options.append(current_option.strip())
                        current_option = line
                    else:
                        # Continuation of the current option
                        if current_option:
                            current_option += " " + line
                        else:
                            # If there's text before any option label, it's part of the question
                            front += line + " "

                # Append the last option
                if current_option:
                    options.append(current_option.strip())

                front = front.strip()

                # Optional: Verify that at least one option starts with "A)"
                if not any(opt.startswith('A)') for opt in options):
                    print(f"Flashcard {idx}: No options starting with 'A)' found. Skipping.")
                    continue
        else:
            front = "No question text found."
            options = []

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
                    # Handle other relative URLs
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
                # Extract the part after 'Answer: ' using partition
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

        # Optional: Print debug information for each flashcard
        # Uncomment the following lines if you need to see the parsed data
        # print(f"Flashcard {idx}:")
        # print(f"Front: {front}")
        # print(f"Options: {options}")
        # print(f"Back: {answer}")
        # print(f"Unit: {unit}")
        # print(f"Chapter: {chapter}")
        # print(f"Images: {images}\n")

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
    index = 1
    chapter = 1
    indexToUrl = {
        1: "https://www.easynotecards.com/notecard_set/89356",
        2: "https://www.easynotecards.com/notecard_set/89357",
        3: "https://www.easynotecards.com/notecard_set/89358",
        4: "https://www.easynotecards.com/notecard_set/89359",
        5: "https://www.easynotecards.com/notecard_set/89360",
        6: "https://www.easynotecards.com/notecard_set/89361",
        7: "https://www.easynotecards.com/notecard_set/89362",
        8: "https://www.easynotecards.com/notecard_set/89363",
        9: "https://www.easynotecards.com/notecard_set/89073",
        10: "https://www.easynotecards.com/notecard_set/89364",
    }


    for i in range(10):
        index += 1
        chapter += 1
        
        scrape_easynotecards_to_json(
            url=indexToUrl[index],
            output_file=f"chapter{chapter}.json",
            unit=f"Chapter {chapter}",
            chapter=f"Chapter {chapter}"
        )

if __name__ == "__main__":
    do()
